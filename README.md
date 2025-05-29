# English Language & Accent Detection Tool 🌍🎯

A tool that first detects if a speaker is speaking English, then analyzes their English accent variety.

## Features

- 🌍 **Language Detection**: Identifies 107+ languages
- 🎯 **English Accent Analysis**: Detects 16 different English accents
- 👔 **Perfect for Recruitment**: Screen English-speaking candidates
- 📞 **Call Center Ready**: Assess language fluency and accent matching

## Supported English Accents

American, British (England), Australian, Indian, Canadian, Scottish, Irish, Welsh, South African, New Zealand, Malaysian, Filipino, Singaporean, Hong Kong, Bermudian, South Atlantic

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/YourUsername/REMProject.git
cd REMProject
```

### 2. Create Virtual Environment
```bash
python -m venv accent-env
source accent-env/bin/activate  # On Windows: accent-env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg
- **Windows**: Download from https://ffmpeg.org/download.html
- **Mac**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

### 5. Run the Application
```bash
streamlit run app.py
```

## Usage

1. Enter a direct video URL (MP4, AVI, MOV, etc.)
2. Click "Analyze Language & Accent"
3. Wait for the two-step analysis:
   - **Step 1**: Language detection
   - **Step 2**: English accent analysis (if English detected)

## File Structure

```
REMProject/
├── app.py              # Streamlit web interface
├── utils.py            # Core detection functions
├── cleanup.py          # Cleanup script for cache files
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Use Cases

- **Recruitment Screening**: Verify English-speaking candidates
- **Call Center Hiring**: Match accents to service regions  
- **Language Assessment**: Determine English fluency levels
- **Quality Control**: Monitor accent consistency

## Notes

- Models will be downloaded automatically on first run
- Cache files are stored in `model_cache/` directory
- Temporary files are cleaned up automatically
- Run `python cleanup.py` to clean cache if needed

## Troubleshooting

If models fail to load, try:
```bash
python cleanup.py  # Clean cache
pip install --upgrade speechbrain transformers
```

## Requirements

- Python 3.8+
- FFmpeg
- 4GB+ RAM (for AI models)
- Internet connection (for model downloads)