# Notes-Taker
A Python script that allows you to be able to record audio and make useful notes of it so that it can be stored in your Google Drive!

## Features
- Record audio from selected microphone(s).
- Creates effective and strong notes through Google's Gemini API of recorded audio
- Automatically stores both recording audio and notes into your Google Drive
- Configurable through environment variables for reusability.

## Requirements
- Python 3.8+ with microphone access
- Installation of portaudio and ffmpeg
- Acquiring API keys from Google Gemini and client secret from Google Drive API
  - Make sure to set the redirect url in the client secret to **http://localhost:8080/**
- Environment variables are properly set

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/notes-synthesizer.git
   cd notes-synthesizer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure `.env`:
   ```plaintext
   GEMINI_API_URL=<KEY>
   ```

4. Run the script:
   ```bash
   python notes_synthesizer_dynamic.py
   ```
