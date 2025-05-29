import streamlit as st
import requests
import os

st.set_page_config(
    page_title="Accent Detection Test", 
    page_icon="🌍", 
    layout="centered"
)

st.title("🌍 Accent Detection Tool (Test Version)")
st.write("Testing deployment...")

# Test basic functionality
if st.button("Test Connection"):
    try:
        # Test requests
        response = requests.get("https://httpbin.org/get", timeout=5)
        st.success("✅ Requests working!")
        
        # Test ffmpeg
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            st.success("✅ FFmpeg working!")
        else:
            st.error("❌ FFmpeg not available")
            
    except Exception as e:
        st.error(f"❌ Error: {e}")

st.info("If you see this, basic deployment is working! Next step: add AI models.")
