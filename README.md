---
title: English Language & Accent Detection
emoji: 🌍
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.36.0
app_file: app.py
pinned: false
---

# English Language & Accent Detection Tool 🌍🎯

A two-step AI tool that first detects if a speaker is speaking English, then analyzes their specific English accent variety. Perfect for recruitment screening and language assessment.

## 🌐 Try It Now!

**Live Demo**: [English Language & Accent Detection on HuggingFace Spaces](https://huggingface.co/spaces/Samimizhr/accent-detection)

*Try the tool directly in your browser - no installation required!*

## 🚀 Features

- **🌍 Language Detection**: Identifies 107+ languages using advanced AI
- **🎯 English Accent Analysis**: Detects 16 different English accent varieties
- **👔 Recruitment Ready**: Screen English-speaking candidates automatically
- **📞 Call Center Optimized**: Assess language fluency and accent matching
- **🔄 Two-Step Process**: Only analyzes accents for confirmed English speakers

## 🎯 Supported English Accents

American, British (England), Australian, Indian, Canadian, Scottish, Irish, Welsh, South African, New Zealand, Malaysian, Filipino, Singaporean, Hong Kong, Bermudian, South Atlantic

## 🛠️ Installation (For Local Development)

Want to run locally or contribute to the project? Follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/ZohrehSamimi/AccentDetection.git
cd AccentDetection
```

### 2. Set Up Environment
```bash
# Create virtual environment
python -m venv accent-env

# Activate virtual environment
# Windows:
accent-env\Scripts\activate
# Mac/Linux:
source accent-env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg
- **Windows**: Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
- **Mac**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

### 5. Run the Application
```bash
# For Gradio version (HuggingFace)
python app.py

# For Streamlit version (Local)
streamlit run app_streamlit.py
```

## 📖 How to Use

1. **Enter Video URL**: Paste a direct video file URL (MP4, AVI, MOV, etc.)
2. **Click Analyze**: Press "Analyze Language & Accent" button
3. **Wait for Results**: The system performs two-step analysis:
   - **Step 1**: Detects if the speaker is speaking English
   - **Step 2**: If English detected, analyzes the specific accent variety

## 📁 Project Structure

```
AccentDetection/
├── app.py              # Gradio web interface (HuggingFace)
├── app_streamlit.py    # Streamlit interface (Local)
├── utils.py            # Core detection functions  
├── cleanup.py          # Cache cleanup utilities
├── requirements.txt    # Python dependencies
├── packages.txt        # System packages (HuggingFace)
├── .gitignore         # Git ignore rules
└── README.md          # This documentation
```

## 💼 Use Cases

- **🏢 Recruitment Screening**: Automatically verify English-speaking candidates
- **📞 Call Center Hiring**: Match candidates to regional service requirements
- **📊 Language Assessment**: Determine English fluency levels objectively
- **🎯 Quality Control**: Monitor accent consistency in voice services
- **📚 Research**: Analyze accent patterns in speech data

## ⚙️ Requirements

- **Python**: 3.8 or higher
- **FFmpeg**: For audio processing
- **RAM**: 4GB+ recommended (AI models)
- **Internet**: Required for initial model downloads
- **Storage**: ~2GB for cached models

## 🔧 Troubleshooting

### Models Won't Load
```bash
python cleanup.py  # Clean model cache
pip install --upgrade speechbrain transformers
```

### Audio Extraction Fails
- Ensure FFmpeg is properly installed
- Check that video URL is a direct file link
- Verify video contains audio track

### Poor Accuracy
- Use videos with clear, single-speaker audio
- Ensure 10+ seconds of continuous speech
- Minimize background noise
- Use high-quality audio recordings

## 📊 Technical Details

- **Language Detection**: SpeechBrain VoxLingua107 (107 languages, 6.7% error rate)
- **Accent Classification**: SpeechBrain ECAPA-TDNN on CommonAccent dataset
- **Audio Processing**: 16kHz mono, PCM format
- **Fallback Methods**: Multiple detection approaches for reliability

## 🗂️ File Management

- **Model Cache**: Stored in `model_cache/` directory
- **Temporary Files**: Auto-cleaned after processing
- **Cache Cleanup**: Run `python cleanup.py` if needed

## ⚡ Performance Notes

- **First Run**: Slower (downloads models ~1-2GB)
- **Subsequent Runs**: Faster (uses cached models)
- **Processing Time**: 30-60 seconds per video
- **Accuracy**: Higher with longer, clearer audio samples

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please check individual model licenses for commercial use.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Ensure all dependencies are installed correctly
3. Verify FFmpeg installation
4. Open an issue on GitHub with error details

---

**Made with ❤️ for multilingual communication and accent diversity**
