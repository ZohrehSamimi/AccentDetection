import gradio as gr
import os
import torch

# Optimize for Hugging Face Spaces
torch.set_num_threads(2)
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# Import your functions
try:
    from utils import download_video, extract_audio, analyze_speech, cleanup_files
except ImportError as e:
    print(f"Import Error: {e}")

def analyze_video_gradio(video_url):
    """
    Main function for Gradio interface
    Returns: (status, language_result, accent_result, confidence_info, detailed_info)
    """
    if not video_url or not video_url.strip():
        return (
            "❌ Error: Please enter a video URL",
            "",
            "",
            "",
            ""
        )
    
    video_path = None
    audio_path = None
    
    try:
        # Download video
        video_path = download_video(video_url.strip())
        
        if not video_path or not os.path.exists(video_path):
            return (
                "❌ Video download failed! Make sure URL is a direct link to video file.",
                "",
                "",
                "",
                "Common issues:\n- URL must be direct link to video file\n- YouTube/social media links won't work\n- Try right-clicking video → 'Copy video address'"
            )
        
        download_info = f"✅ Video downloaded ({os.path.getsize(video_path):,} bytes)"
        
        # Extract audio
        audio_path = extract_audio(video_path)
        
        if not audio_path or not os.path.exists(audio_path):
            return (
                "❌ Audio extraction failed! Video might not contain audio.",
                "",
                "",
                "",
                "The video file doesn't contain audio or is in an unsupported format."
            )
        
        audio_info = f"✅ Audio extracted ({os.path.getsize(audio_path):,} bytes)"
        
        # Analyze speech
        is_english, language, accent, lang_confidence, accent_confidence = analyze_speech(audio_path)
        
        if not is_english:
            # NOT ENGLISH
            status = "❌ Speaker is NOT speaking English"
            language_result = f"Detected Language: {language.title()}"
            accent_result = "N/A (Not English)"
            confidence_info = f"Language Confidence: {lang_confidence:.1f}%"
            detailed_info = f"""
{download_info}
{audio_info}

ANALYSIS RESULTS:
Language: {language.title()}
Confidence: {lang_confidence:.1f}%

For English accent analysis, please provide a video where the speaker is speaking English.
            """.strip()
            
        else:
            # IS ENGLISH
            status = "✅ Speaker IS speaking English!"
            language_result = "Language: English ✅"
            accent_result = f"Detected Accent: {accent}"
            confidence_info = f"Language: {lang_confidence:.1f}% | Accent: {accent_confidence:.1f}%"
            
            # Confidence interpretation
            if accent_confidence >= 80:
                confidence_desc = "🎯 High confidence prediction"
            elif accent_confidence >= 60:
                confidence_desc = "🤔 Moderate confidence prediction"
            else:
                confidence_desc = "⚠️ Low confidence prediction"
            
            # Recruitment assessment
            if lang_confidence >= 80:
                recruitment_status = "✅ CANDIDATE SPEAKS ENGLISH - Suitable for English-speaking roles"
            elif lang_confidence >= 60:
                recruitment_status = "🤔 LIKELY SPEAKS ENGLISH - May need additional assessment"
            else:
                recruitment_status = "⚠️ UNCERTAIN - Recommend manual review"
            
            detailed_info = f"""
{download_info}
{audio_info}

🎯 AI ANALYSIS RESULTS:
Language: English
Language Confidence: {lang_confidence:.1f}%
Detected Accent: {accent}
Accent Confidence: {accent_confidence:.1f}%
Assessment: {confidence_desc}

👔 FOR RECRUITERS:
{recruitment_status}

🔬 TECHNICAL DETAILS:
- Language Model: SpeechBrain VoxLingua107 (107 languages)
- Accent Model: SpeechBrain ECAPA-TDNN (CommonAccent dataset)
- Audio Processing: 16kHz mono PCM
- Supported Accents: American, British, Australian, Indian, Canadian, Scottish, Irish, Welsh, South African, New Zealand, Malaysian, Filipino, Singaporean, Hong Kong, Bermudian, South Atlantic

💡 FACTORS AFFECTING ACCURACY:
- Audio quality and clarity
- Background noise levels
- Speaker's accent strength  
- Length of speech (10+ seconds recommended)
- Speaking style and pace
            """.strip()
        
        return (status, language_result, accent_result, confidence_info, detailed_info)
        
    except Exception as e:
        error_details = f"Error: {str(e)}"
        return (
            "❌ Analysis failed",
            "",
            "",
            "",
            f"Unexpected error occurred:\n{error_details}\n\nTry:\n- Different video with clearer audio\n- Ensure video contains 10+ seconds of speech\n- Check audio quality"
        )
    
    finally:
        # Clean up temporary files
        if video_path or audio_path:
            cleanup_files(video_path, audio_path)

# Create Gradio interface
def create_interface():
    with gr.Blocks(
        title="English Language & Accent Detection",
        theme=gr.themes.Soft(),
        css=".gradio-container {max-width: 900px; margin: auto;}"
    ) as interface:
        
        gr.HTML("""
        <div style="text-align: center; padding: 20px;">
            <h1>🌍 English Language & Accent Detection Tool</h1>
            <p>AI-powered tool that detects if a speaker is speaking English, then analyzes their accent variety.</p>
            <p><strong>🤗 Running on Hugging Face Spaces - Free AI analysis!</strong></p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column():
                video_url_input = gr.Textbox(
                    label="🔗 Video URL",
                    placeholder="https://example.com/video.mp4",
                    info="Enter a direct link to a video file (MP4, AVI, MOV, etc.)"
                )
                
                analyze_btn = gr.Button(
                    "🔍 Analyze Language & Accent", 
                    variant="primary",
                    size="lg"
                )
        
        with gr.Row():
            status_output = gr.Textbox(
                label="📊 Analysis Status",
                interactive=False
            )
        
        with gr.Row():
            with gr.Column():
                language_output = gr.Textbox(
                    label="🌍 Language Detection",
                    interactive=False
                )
            with gr.Column():
                accent_output = gr.Textbox(
                    label="🎯 Accent Detection", 
                    interactive=False
                )
        
        confidence_output = gr.Textbox(
            label="📈 Confidence Scores",
            interactive=False
        )
        
        detailed_output = gr.Textbox(
            label="📋 Detailed Results",
            interactive=False,
            lines=15
        )
        
        # How it works section
        with gr.Accordion("ℹ️ How this tool works", open=False):
            gr.HTML("""
            <h3>Two-Step AI Analysis:</h3>
            <h4>Step 1: Language Detection 🌍</h4>
            <ul>
                <li><strong>AI model analyzes audio</strong> to identify spoken language</li>
                <li><strong>Supports 107+ languages</strong> using SpeechBrain VoxLingua107</li>
                <li><strong>Only proceeds if English detected</strong></li>
            </ul>
            
            <h4>Step 2: English Accent Analysis 🎯</h4>
            <ul>
                <li><strong>16 different English accents:</strong></li>
                <li>American, British (England), Australian, Indian, Canadian</li>
                <li>Scottish, Irish, Welsh, South African, New Zealand</li>
                <li>Malaysian, Filipino, Singaporean, Hong Kong, Bermudian, South Atlantic</li>
            </ul>
            
            <h3>Perfect for:</h3>
            <ul>
                <li>✅ <strong>Recruitment screening</strong> - Verify English-speaking candidates</li>
                <li>✅ <strong>Language assessment</strong> - Determine English fluency levels</li>
                <li>✅ <strong>Call center hiring</strong> - Match accents to service regions</li>
                <li>✅ <strong>Research & analysis</strong> - Study accent patterns</li>
            </ul>
            
            <h3>Requirements:</h3>
            <ul>
                <li>Direct video file URL (not YouTube/social media links)</li>
                <li>Clear audio with minimal background noise</li>
                <li>At least 10-15 seconds of speech</li>
                <li>Single speaker preferred</li>
            </ul>
            """)
        
        # Use cases section  
        with gr.Accordion("🎯 Use Cases", open=False):
            gr.HTML("""
            <div style="display: flex; justify-content: space-around;">
                <div>
                    <h4>🏢 Recruitment & HR:</h4>
                    <ul>
                        <li>Screen English-speaking candidates</li>
                        <li>Verify language requirements</li>
                        <li>Assess communication skills</li>
                        <li>Filter initial applications</li>
                    </ul>
                </div>
                <div>
                    <h4>📞 Business Applications:</h4>
                    <ul>
                        <li>Call center agent assessment</li>
                        <li>Voice training programs</li>
                        <li>Accent coaching feedback</li>
                        <li>Quality assurance checks</li>
                    </ul>
                </div>
            </div>
            """)
        
        # Connect the interface
        analyze_btn.click(
            fn=analyze_video_gradio,
            inputs=[video_url_input],
            outputs=[status_output, language_output, accent_output, confidence_output, detailed_output]
        )
        
        gr.HTML("""
        <div style="text-align: center; margin-top: 20px; color: #666; font-size: 0.9em;">
            🤗 Powered by Hugging Face Spaces • 🧠 AI Models: SpeechBrain<br>
            🌍 Language Detection → 🎯 English Accent Analysis<br>
            Made with ❤️ for multilingual communication
        </div>
        """)
    
    return interface

# Launch the interface
if __name__ == "__main__":
    interface = create_interface()
    interface.launch()
