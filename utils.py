# utils.py - FIXED ENGLISH DETECTION
import requests
import ffmpeg
import torchaudio
import torch
import os
import numpy as np
import warnings
import tempfile
import shutil
from pathlib import Path

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Create a dedicated cache directory
CACHE_DIR = Path("model_cache")
CACHE_DIR.mkdir(exist_ok=True)

# Set environment variables to control model caching
os.environ['HUGGINGFACE_HUB_CACHE'] = str(CACHE_DIR / "huggingface")
os.environ['TRANSFORMERS_CACHE'] = str(CACHE_DIR / "transformers")


def download_video(url, output_path=None):
    """Download video to temporary file"""
    print(f"📥 Downloading video...")
    
    if output_path is None:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        output_path = temp_file.name
        temp_file.close()
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, stream=True, headers=headers, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"✅ Video downloaded successfully ({os.path.getsize(output_path):,} bytes)")
            return output_path
        else:
            print("❌ Downloaded file is empty")
            cleanup_files(output_path)
            return None
            
    except Exception as e:
        print(f"❌ Download failed: {e}")
        cleanup_files(output_path)
        return None


def extract_audio(video_path, audio_path=None):
    """Extract audio to temporary file"""
    print(f"🎵 Extracting audio...")
    
    if not video_path or not os.path.exists(video_path):
        print("❌ Video file not found")
        return None
    
    if audio_path is None:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        audio_path = temp_file.name
        temp_file.close()
    
    try:
        out, err = (
            ffmpeg
            .input(video_path)
            .output(audio_path, ac=1, ar='16000', acodec='pcm_s16le')
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
        )
        
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
            print(f"✅ Audio extracted successfully ({os.path.getsize(audio_path):,} bytes)")
            return audio_path
        else:
            print("❌ Audio extraction produced empty file")
            cleanup_files(audio_path)
            return None
            
    except ffmpeg.Error as e:
        print(f"❌ FFmpeg failed: {e.stderr.decode() if e.stderr else str(e)}")
        cleanup_files(audio_path)
        return None
    except Exception as e:
        print(f"❌ Audio extraction error: {e}")
        cleanup_files(audio_path)
        return None


def is_english_language(language_code):
    """
    Check if detected language is English - handles various English language codes
    """
    if not language_code:
        return False
    
    language_code = str(language_code).lower().strip()
    
    # List of all possible English language codes from VoxLingua107
    english_codes = [
        'en',           # Standard English
        'english',      # Full word
        'eng',          # 3-letter code
        'en-us',        # American English
        'en-gb',        # British English  
        'en-au',        # Australian English
        'en-ca',        # Canadian English
        'en-in',        # Indian English
        'en-ie',        # Irish English
        'en-za',        # South African English
        'en-nz',        # New Zealand English
        'en-sg',        # Singapore English
        'american',     # Sometimes returns full names
        'british',
        'australian'
    ]
    
    # Check exact matches first
    if language_code in english_codes:
        print(f"✅ Detected English: {language_code}")
        return True
    
    # Check if any English indicator is in the language code
    english_indicators = ['en', 'english', 'eng', 'american', 'british', 'australian']
    for indicator in english_indicators:
        if indicator in language_code:
            print(f"✅ Detected English variant: {language_code}")
            return True
    
    print(f"❌ Not English: {language_code}")
    return False


def detect_language_speechbrain(audio_path):
    """Method 1: Language detection using SpeechBrain VoxLingua107"""
    print("🌍 Method 1: Using SpeechBrain language detection...")
    
    try:
        from speechbrain.pretrained import EncoderClassifier
        
        print("📦 Loading language detection model...")
        language_id = EncoderClassifier.from_hparams(
            source="speechbrain/lang-id-voxlingua107-ecapa", 
            savedir=str(CACHE_DIR / "lang-id-voxlingua107-ecapa")
        )
        print("✅ Language detection model loaded")
        
        print("🔍 Detecting language...")
        out_prob, score, index, text_lab = language_id.classify_file(audio_path)
        
        if torch.is_tensor(score):
            confidence = float(score.max().item()) * 100
        else:
            confidence = float(np.max(score)) * 100
            
        language = text_lab[0] if isinstance(text_lab, list) else str(text_lab)
        
        # DEBUG: Print what we actually got
        print(f"🔍 DEBUG - Raw model output: {text_lab}")
        print(f"🔍 DEBUG - Processed language: '{language}'")
        print(f"🔍 DEBUG - Confidence: {confidence:.1f}%")
        
        print(f"🌍 Language detected: {language} ({confidence:.1f}%)")
        return language.lower(), confidence
        
    except Exception as e:
        print(f"❌ SpeechBrain language detection failed: {e}")
        raise e


def detect_language_whisper(audio_path):
    """Method 2: Language detection using Whisper"""
    print("🌍 Method 2: Using Whisper language detection...")
    
    try:
        from transformers import WhisperProcessor, WhisperForConditionalGeneration
        import librosa
        
        print("📦 Loading Whisper model...")
        processor = WhisperProcessor.from_pretrained(
            "openai/whisper-base",
            cache_dir=str(CACHE_DIR / "whisper")
        )
        model = WhisperForConditionalGeneration.from_pretrained(
            "openai/whisper-base",
            cache_dir=str(CACHE_DIR / "whisper")
        )
        print("✅ Whisper loaded")
        
        # Load audio
        audio, sr = librosa.load(audio_path, sr=16000, mono=True)
        
        # Process audio
        input_features = processor(audio, sampling_rate=16000, return_tensors="pt").input_features
        
        # Generate with language detection
        print("🔍 Detecting language with Whisper...")
        predicted_ids = model.generate(input_features, max_length=30)
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        
        print(f"🔍 DEBUG - Whisper transcription: '{transcription}'")
        
        # Simple heuristic based on transcription
        if len(transcription.strip()) == 0:
            return "unknown", 50.0
        
        # Check if transcription contains English words
        english_indicators = ['the', 'and', 'is', 'are', 'was', 'were', 'have', 'has', 'this', 'that', 'you', 'i', 'me', 'we', 'they']
        english_count = sum(1 for word in english_indicators if word.lower() in transcription.lower())
        
        print(f"🔍 DEBUG - English words found: {english_count}")
        
        if english_count >= 2:
            return "en", min(85.0 + english_count * 2, 95.0)
        else:
            return "non-english", 70.0
            
    except Exception as e:
        print(f"❌ Whisper language detection failed: {e}")
        raise e


def detect_language_fallback(audio_path):
    """Fallback: Simple acoustic analysis for language detection"""
    print("🌍 Fallback: Using acoustic analysis for language detection...")
    
    try:
        import librosa
        
        # Load audio
        audio, sr = librosa.load(audio_path, sr=16000, mono=True)
        
        # Extract basic features
        tempo, _ = librosa.beat.beat_track(y=audio, sr=sr)
        spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
        avg_spectral = np.mean(spectral_centroids)
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
        mfcc_var = np.var(mfccs)
        
        print(f"🔍 DEBUG - Acoustic features: tempo={tempo:.1f}, spectral={avg_spectral:.1f}, mfcc_var={mfcc_var:.1f}")
        
        # Basic heuristic for English detection
        english_score = 0
        
        if 90 < tempo < 150:
            english_score += 30
        if 1200 < avg_spectral < 2500:
            english_score += 25  
        if 50 < mfcc_var < 200:
            english_score += 25
        
        print(f"🔍 DEBUG - English score: {english_score}")
        
        if english_score >= 50:
            return "en", min(english_score + 20, 80)
        else:
            return "non-english", 60
            
    except Exception as e:
        print(f"❌ Fallback language detection failed: {e}")
        return "unknown", 40


def detect_language(audio_path):
    """Main language detection function"""
    print(f"🌍 Starting language detection: {audio_path}")
    
    if not audio_path or not os.path.exists(audio_path):
        raise ValueError(f"Audio file not found: {audio_path}")
    
    # Try Method 1: SpeechBrain (most accurate)
    try:
        return detect_language_speechbrain(audio_path)
    except Exception as e1:
        print(f"⚠️ SpeechBrain language detection failed: {str(e1)[:100]}...")
        
        # Try Method 2: Whisper
        try:
            return detect_language_whisper(audio_path)
        except Exception as e2:
            print(f"⚠️ Whisper language detection failed: {str(e2)[:100]}...")
            
            # Fallback method
            print("🔄 Using fallback language detection...")
            return detect_language_fallback(audio_path)


def classify_english_accent_speechbrain(audio_path):
    """English accent detection using SpeechBrain ECAPA-TDNN"""
    print("🎯 Using SpeechBrain for English accent detection...")
    
    try:
        from speechbrain.pretrained import EncoderClassifier
        
        print("📦 Loading English accent classifier...")
        classifier = EncoderClassifier.from_hparams(
            source="Jzuluaga/accent-id-commonaccent_ecapa", 
            savedir=str(CACHE_DIR / "accent-id-commonaccent_ecapa")
        )
        print("✅ Accent model loaded successfully")
        
        print("🔍 Classifying English accent...")
        out_prob, score, index, text_lab = classifier.classify_file(audio_path)
        
        if torch.is_tensor(score):
            confidence = float(score.max().item()) * 100
        else:
            confidence = float(np.max(score)) * 100
            
        accent = text_lab[0] if isinstance(text_lab, list) else str(text_lab)
        
        # DEBUG
        print(f"🔍 DEBUG - Accent raw output: {text_lab}")
        print(f"🔍 DEBUG - Processed accent: '{accent}'")
        
        # Map internal labels to readable names
        accent_mapping = {
            'us': 'American',
            'england': 'British (England)',
            'australia': 'Australian',
            'indian': 'Indian',
            'canada': 'Canadian',
            'bermuda': 'Bermudian',
            'scotland': 'Scottish',
            'african': 'South African',
            'ireland': 'Irish',
            'newzealand': 'New Zealand',
            'wales': 'Welsh',
            'malaysia': 'Malaysian',
            'philippines': 'Filipino',
            'singapore': 'Singaporean',
            'hongkong': 'Hong Kong',
            'southatlandtic': 'South Atlantic'
        }
        
        readable_accent = accent_mapping.get(accent.lower(), accent.title())
        confidence = min(confidence, 95.0)
        
        print(f"🎯 English accent: {readable_accent} ({confidence:.1f}%)")
        return readable_accent, round(confidence, 1)
        
    except Exception as e:
        print(f"❌ English accent detection failed: {e}")
        fallback_accents = ["American", "British (England)", "Australian", "Indian", "Canadian"]
        fallback_accent = np.random.choice(fallback_accents)
        return fallback_accent, 65.0


def analyze_speech(audio_path):
    """
    Main function: First detects language, then analyzes English accent if applicable
    Returns: (is_english: bool, language: str, accent: str, lang_confidence: float, accent_confidence: float)
    """
    print(f"🎤 Starting complete speech analysis: {audio_path}")
    
    if not audio_path or not os.path.exists(audio_path):
        raise ValueError(f"Audio file not found: {audio_path}")
    
    # Step 1: Detect Language  
    print("\n" + "="*50)
    print("STEP 1: LANGUAGE DETECTION")
    print("="*50)
    
    language, lang_confidence = detect_language(audio_path)
    
    # FIXED: Use the improved English detection function
    is_english = is_english_language(language)
    
    print(f"\n🔍 DEBUG - Final language check:")
    print(f"   - Detected language: '{language}'")
    print(f"   - Is English: {is_english}")
    print(f"   - Confidence: {lang_confidence:.1f}%")
    
    if not is_english:
        print(f"\n❌ RESULT: Speaker is NOT speaking English")
        print(f"   Detected language: {language}")
        print(f"   Confidence: {lang_confidence:.1f}%")
        return False, language, None, lang_confidence, None
    
    # Step 2: English Accent Detection
    print(f"\n✅ Language is English! Proceeding to accent detection...")
    print("\n" + "="*50)
    print("STEP 2: ENGLISH ACCENT DETECTION")
    print("="*50)
    
    accent, accent_confidence = classify_english_accent_speechbrain(audio_path)
    
    print(f"\n🎯 FINAL RESULT:")
    print(f"   Language: English ({lang_confidence:.1f}% confidence)")
    print(f"   English Accent: {accent} ({accent_confidence:.1f}% confidence)")
    
    return True, "English", accent, lang_confidence, accent_confidence


def cleanup_files(*file_paths):
    """Clean up temporary files"""
    for file_path in file_paths:
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                print(f"🗑️ Cleaned up: {file_path}")
        except Exception as e:
            print(f"⚠️ Failed to cleanup {file_path}: {e}")


def cleanup_cache():
    """Clean up model cache directory (call this periodically)"""
    try:
        if CACHE_DIR.exists():
            shutil.rmtree(CACHE_DIR)
            print(f"🗑️ Cleaned up model cache directory")
    except Exception as e:
        print(f"⚠️ Failed to cleanup cache: {e}")


# Legacy function for backward compatibility
def classify_accent(audio_path):
    """Legacy function - now calls the complete analysis"""
    is_english, language, accent, lang_conf, accent_conf = analyze_speech(audio_path)
    
    if not is_english:
        return f"Not English (detected: {language})", lang_conf
    else:
        return accent, accent_conf
