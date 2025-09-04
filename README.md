# WhatsApp Multilingual STT & TTS Project

A Streamlit-based web application that provides multilingual Speech-to-Text (STT) and Text-to-Speech (TTS) capabilities using Google Cloud Speech-to-Text and Text-to-Speech APIs.

## Features

- **Multilingual Support**: Supports 10+ Indian languages including English, Hindi, Tamil, Telugu, Malayalam, Kannada, Bengali, Marathi, Gujarati, and Punjabi
- **Speech-to-Text**: Upload WAV audio files for transcription
- **Text-to-Speech**: Convert text to speech with various voice options
- **Hinglish Support**: Special handling for Hinglish (Hindi-English mix)
- **Voice Selection**: Choose from different voice options for each language

## Prerequisites

- Python 3.7 or higher
- Google Cloud Platform account with Speech-to-Text and Text-to-Speech APIs enabled
- Google Cloud service account credentials JSON file
- FFmpeg (for audio processing) - Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd whatsapp_proj
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Google Cloud credentials:
   - Download your service account JSON key file
   - Update the path in `main.py` line 10:
   ```python
   os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"path/to/your/credentials.json"
   ```

## Usage

1. **Important**: Make sure to run the app with the correct command:
```bash
streamlit run main.py
```
**Do NOT use** `python main.py` as it will cause session state errors.

2. Open your browser and navigate to the provided local URL (usually `http://localhost:8501`)

3. Follow the on-screen instructions:
   - Select your preferred language
   - For STT: Upload a WAV audio file (16kHz, mono)
   - For TTS: Enter text and select a voice option

## Supported Languages

- English (India)
- Hindi
- Hinglish
- Tamil
- Telugu
- Malayalam
- Kannada
- Bengali
- Marathi
- Gujarati
- Punjabi

## Audio Requirements

- **Format**: WAV files
- **Sample Rate**: 16kHz
- **Channels**: Mono

## Project Structure

```
whatsapp_proj/
├── main.py              # Main Streamlit application
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
