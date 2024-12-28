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
  - Make sure to set the redirect url to **http://localhost:8080/**
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
   API_URL=https://your-canvas-api-url
   API_KEY=your-canvas-api-key
   COURSE_ID=your-course-id
   INSTITUTION_URL=https://your-institution-url
   NOTE_FOLDER_DIRECTORY=/path/to/your/notes
   COMBINED_NOTES_DIRECTORY=/path/to/output/combined-notes.pdf
   SENDER_EMAIL=your-email@example.com
   RECEIVER_EMAIL=receiver-email@example.com
   EMAIL_PASSWORD=your-email-password
   MODULE_ITEM_IDS=[]
   ```

4. Run the script:
   ```bash
   python notes_synthesizer_dynamic.py
   ```
