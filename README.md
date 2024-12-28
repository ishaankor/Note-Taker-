# Notes-Taker
A Python script that allows you to be able to record audio and make useful notes of it so that it can be stored in your Google Drive!

## Features
- Record audio from selected microphone(s).
- Creates effective and strong notes through Google's Gemini API of recorded audio
- Automatically stores both recording audio and notes into your Google Drive
- Configurable through environment variables for reusability.

## System Dependencies

This project requires the following system dependencies:

1. **PortAudio** (for `pyaudio`):
   - Linux: `sudo apt-get install portaudio19-dev`
   - MacOS: `brew install portaudio`
   - Windows: Use `pipwin` to install `pyaudio`:
     ```bash
     pip install pipwin
     pipwin install pyaudio
     ```

2. **FFmpeg** (for `pydub`):
   - Linux: `sudo apt-get install ffmpeg`
   - MacOS: `brew install ffmpeg`
   - Windows: Download and configure FFmpeg:
     - [FFmpeg Download](https://ffmpeg.org/download.html)
     - Add FFmpeg to your system PATH.

## Requirements
- Python 3.8+ with microphone access
- Installation of system-level dependencies like portaudio and ffmpeg
- Acquiring API keys from Google Gemini and client secret from Google Drive API
  - Make sure to set the redirect url in the client secret to **http://localhost:8080/**
- Environment variables are properly set

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ishaankor/notes-taker.git
   cd notes-taker
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
   python notes-taker.py
   ```
