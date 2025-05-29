# app.py - FIXED VERSION
import streamlit as st
import os
import sys

# MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="English Language & Accent Detection", 
    page_icon="🌍", 
    layout="centered"
)

# STREAMLIT CLOUD OPTIMIZATIONS
import torch
torch.set_num_threads(1)  # Reduce CPU usage
os.environ['TOKENIZERS_PARALLELISM'] = 'false'  # Avoid threading issues

# Add error handling for imports
try:
    from utils import download_video, extract_audio, analyze_speech, cleanup_files
except ImportError as e:
    st.error(f"❌ Import Error: {e}")
    st.info("This might be a deployment issue. Please check the logs.")
    st.stop()

st.title("🌍 English Language & Accent Detection Tool")
st.write("Upload a video to first detect if the speaker is speaking English, then analyze their English accent.")

# Add a warning for Streamlit Cloud users
st.info("⚠️ **Note**: First-time model loading may take 2-3 minutes. Please be patient!")

# Information section
with st.expander("ℹ️ How this tool works"):
    st.write("""
    ## Two-Step Analysis Process:
    
    ### Step 1: Language Detection 🌍
    - **Detects what language** the speaker is using
    - **Supports 107+ languages** using advanced AI models
    - **Only proceeds to accent analysis** if English is detected
    
    ### Step 2: English Accent Analysis 🎯 (Only if English detected)
    - **16 different English accents** can be identified:
      - American, British (England), Australian, Indian, Canadian
      - Scottish, Irish, Welsh, South African, New Zealand
      - Malaysian, Filipino, Singaporean, Hong Kong, Bermudian, South Atlantic
    
    ## Perfect for:
    ✅ **Recruitment screening** - Verify English language candidates  
    ✅ **Language assessment** - Determine if applicant speaks English  
    ✅ **Accent identification** - Identify specific English accent varieties  
    ✅ **Call center hiring** - Screen for English-speaking candidates  
    
    ## Requirements:
    - Direct video file URL (MP4, AVI, MOV, etc.)
    - Clear audio with minimal background noise
    - At least 10-15 seconds of speech
    - Single speaker preferred
    """)

# URL input
video_url = st.text_input(
    "🔗 Video URL:", 
    placeholder="https://example.com/video.mp4",
    help="Enter a direct link to a video file"
)

# Analysis button
if st.button("🔍 Analyze Language & Accent", type="primary"):
    if not video_url.strip():
        st.warning("⚠️ Please enter a video URL first.")
    else:
        video_path = None
        audio_path = None
        
        try:
            # Download video
            with st.spinner("📥 Downloading video..."):
                video_path = download_video(video_url.strip())
                
                if not video_path or not os.path.exists(video_path):
                    st.error("❌ **Video download failed!**")
                    st.write("**Possible reasons:**")
                    st.write("- URL is not a direct link to a video file")
                    st.write("- Video is behind authentication/login")
                    st.write("- Server is blocking requests")
                    st.write("- URL is incorrect or video doesn't exist")
                    st.stop()
                
                st.success(f"✅ Video downloaded ({os.path.getsize(video_path):,} bytes)")

            # Extract audio
            with st.spinner("🎵 Extracting audio..."):
                audio_path = extract_audio(video_path)
                
                if not audio_path or not os.path.exists(audio_path):
                    st.error("❌ **Audio extraction failed!**")
                    st.write("**Possible reasons:**")
                    st.write("- Video file is corrupted")
                    st.write("- Video format not supported")  
                    st.write("- Video has no audio track")
                    st.write("- FFmpeg is not properly installed")
                    st.stop()
                
                st.success(f"✅ Audio extracted ({os.path.getsize(audio_path):,} bytes)")

            # Analyze speech
            with st.spinner("🧠 Analyzing language and accent... This may take 2-3 minutes on first run..."):
                try:
                    is_english, language, accent, lang_confidence, accent_confidence = analyze_speech(audio_path)
                    
                    # Display results
                    st.markdown("---")
                    st.markdown("### 🎯 Analysis Results")
                    
                    if not is_english:
                        # NOT ENGLISH
                        st.error("❌ **Speaker is NOT speaking English**")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric(
                                label="Detected Language", 
                                value=language.title()
                            )
                        with col2:
                            st.metric(
                                label="Confidence", 
                                value=f"{lang_confidence:.1f}%"
                            )
                        
                        st.info("💡 **For English accent analysis, please provide a video where the speaker is speaking English.**")
                        
                        with st.expander("🌍 About Language Detection"):
                            st.write(f"""
                            **Detected Language:** {language.title()}  
                            **Detection Confidence:** {lang_confidence:.1f}%
                            
                            This tool first detects what language is being spoken before proceeding to accent analysis. 
                            Since the speaker appears to be speaking **{language.title()}** rather than English, 
                            we cannot proceed with English accent detection.
                            
                            **To get English accent analysis:**
                            - Provide a video where the speaker is clearly speaking English
                            - Ensure the audio quality is good
                            - Make sure there's at least 10-15 seconds of speech
                            """)
                    
                    else:
                        # IS ENGLISH - Show accent results
                        st.success("✅ **Speaker IS speaking English!**")
                        
                        # Main metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric(
                                label="Language", 
                                value="English ✅"
                            )
                        with col2:
                            st.metric(
                                label="Detected Accent", 
                                value=accent
                            )
                        with col3:
                            st.metric(
                                label="Accent Confidence", 
                                value=f"{accent_confidence:.1f}%"
                            )
                        
                        # Confidence interpretation
                        if accent_confidence >= 80:
                            st.success("🎯 High confidence accent prediction")
                        elif accent_confidence >= 60:
                            st.info("🤔 Moderate confidence accent prediction")
                        else:
                            st.warning("⚠️ Low confidence accent prediction - results may be unreliable")
                        
                        # Detailed results
                        with st.expander("📊 Detailed Analysis Results"):
                            st.write(f"""
                            ### Language Detection Results:
                            **Language:** English  
                            **Language Confidence:** {lang_confidence:.1f}%
                            
                            ### English Accent Analysis:
                            **Detected Accent:** {accent}  
                            **Accent Confidence:** {accent_confidence:.1f}%
                            
                            ### Interpretation:
                            The AI first confirmed that the speaker is speaking English with {lang_confidence:.1f}% confidence.
                            Then it analyzed the English accent and detected **{accent}** accent patterns 
                            with {accent_confidence:.1f}% confidence.
                            
                            ### Factors affecting accuracy:
                            - Audio quality and clarity
                            - Background noise levels  
                            - Speaker's accent strength
                            - Length of speech sample
                            - Speaking style and pace
                            
                            ### Supported English Accents:
                            American, British (England), Australian, Indian, Canadian, Scottish, Irish, Welsh, 
                            South African, New Zealand, Malaysian, Filipino, Singaporean, Hong Kong, Bermudian, South Atlantic
                            """)
                        
                        # For recruiters
                        st.markdown("### 👔 For Recruiters & HR:")
                        if lang_confidence >= 80:
                            st.success("✅ **CANDIDATE SPEAKS ENGLISH** - Suitable for English-speaking roles")
                        elif lang_confidence >= 60:
                            st.info("🤔 **LIKELY SPEAKS ENGLISH** - May need additional assessment")
                        else:
                            st.warning("⚠️ **UNCERTAIN** - Recommend manual review or additional testing")
                        
                except Exception as e:
                    st.error("❌ **Analysis failed!**")
                    st.write("**Error details:**")
                    st.code(str(e))
                    st.write("**Possible solutions:**")
                    st.write("- Try a different video with clearer audio")
                    st.write("- Ensure the video contains clear speech (any language)")
                    st.write("- Check that the audio is at least 10-15 seconds long")
                    st.write("- Verify the video URL is accessible")

        except Exception as e:
            st.error(f"❌ **Unexpected error occurred:**")
            st.code(str(e))
            st.write("Please try again with a different video or contact support if the issue persists.")
        
        finally:
            # Clean up temporary files
            if video_path or audio_path:
                cleanup_files(video_path, audio_path)

# Use cases section
st.markdown("---")
st.markdown("### 🎯 Use Cases")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **🏢 For Recruitment:**
    - Screen English-speaking candidates
    - Verify language requirements
    - Identify accent preferences
    - Filter initial applications
    """)

with col2:
    st.markdown("""
    **📞 For Call Centers:**
    - Assess English fluency
    - Match accents to regions
    - Quality control checks
    - Training needs assessment
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
    🌍 This tool first detects if the speaker is speaking English, then analyzes their English accent.<br>
    Perfect for recruitment screening and language assessment.<br>
    Results are AI-generated estimates and may not always be 100% accurate.
    </div>
    """, 
    unsafe_allow_html=True
)
