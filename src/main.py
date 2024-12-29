import os
import google.generativeai as genai
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from dotenv import load_dotenv
import speech_recognition as sr
from pydub import AudioSegment
from datetime import datetime
import wave
import json
import pyaudio
import threading
import whisper

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

recording = True
current_name = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
root_directory_id = None
audio_directory_id = None
note_directory_id = None


# Check that the appropriate variables are accessible
def check_credentials():
    if not os.path.exists('audio_file.wav'):
        print("Created new template audio file!")
        audio_file = AudioSegment.empty()
        audio_file.export("audio_file.wav", format="wav")
    if GEMINI_API_KEY == "<KEY>":
        exit("Please get your Gemini API key!")
    if not os.path.exists('client_secret.json'):
        exit("Please grab the client secret JSON from your Google Drive API!")
    else:
        client_secret_file = open('client_secret.json', 'r')
        client_secret_json = json.load(client_secret_file)
        print(client_secret_json['web'])
        if 'redirect_uris' not in client_secret_json['web'].keys():
            exit('Please make sure to make the "redirect_uris" key in your client_secret.json equal to "http://localhost:8080/" or any other url you would like to use!')


def record_audio(audio_file):
    """Continuously records audio until the recording flag is set to False."""
    global recording
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100
    p = pyaudio.PyAudio()
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)
    frames = []
    while recording:
        data = stream.read(chunk, exception_on_overflow=False)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    with wave.open(audio_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
    print(f"Audio saved to {audio_file}")


def initalize_remaining_folders(drive):
    global root_directory_id, audio_directory_id, note_directory_id
    if root_directory_id is None:
        print("Created the root directory!")
        folder_metadata = {
            "title": "Note Taker!",
            "mimeType": "application/vnd.google-apps.folder"
        }
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
        root_directory_id = folder['id']
    if audio_directory_id is None:
        print("Created the audio directory!")
        folder_metadata = {
            "title": "Lecture Audio",
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [{"id": root_directory_id}]
        }
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
        audio_directory_id = folder['id']
    if note_directory_id is None:
        print("Created the notes directory!")
        folder_metadata = {
            "title": "Lecture Notes",
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [{"id": root_directory_id}]
        }
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
        note_directory_id = folder['id']


# Authenticate Google Drive using client secrets
def authenticate_google_drive():
    global root_directory_id, audio_directory_id, note_directory_id
    print("Authenticating Google Drive...")
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile("client_secret.json")
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    print("Google Drive authentication successful!")
    folder_list = drive.ListFile({'q': "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    try:
        for folder in folder_list:
            if folder['title'] == "Note Taker!":
                print("Found the root directory!")
                root_directory_id = folder['id']
                try:
                    query = f"'{folder['id']}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
                    folder_list = drive.ListFile({'q': query}).GetList()
                    # print(f"Folders in folder ID {root_directory_id}:")
                    for folders in folder_list:
                        if folders['title'] == "Lecture Audio":
                            print("Found the audio directory!")
                            audio_directory_id = folders['id']
                    for folders in folder_list:
                        if folders['title'] == "Lecture Notes":
                            print("Found the notes directory!")
                            note_directory_id = folders['id']
                        print(f"Name: {folders['title']}, ID: {folders['id']}")
                except Exception as e:
                    print(f"Error retrieving folders: {e}")
                    return []
                finally:
                    initalize_remaining_folders(drive)
                    return drive
    except Exception as e:
        print(f"Error retrieving folders: {e}")
    initalize_remaining_folders(drive)
    return drive


# Transcribe lecture audio
def interpret_lecture(filename):
    model = whisper.load_model("turbo")
    result = model.transcribe(filename, fp16=False)  # make fp16 equal to false if shown a warning
    return result["text"]


# Transform transcript into effective notes using OpenAI GPT
def synthesizing_lecture(audio_transcript):
    print("Processing notes with Google's Gemini...")
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        exit("Please get your Gemini API key!")
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        prompt = (
            f"Turn this transcript into effective notes with key elements, summaries, and action points: \n\n {audio_transcript}")
        synthesized_notes = model.generate_content(prompt)
        print("Notes synthesized successfully.")
        print(synthesized_notes.text)
        return synthesized_notes.text
    except Exception as e:
        print(f"Error during Gemini processing: {e}")
        return None


# Upload notes to a specific Google Drive folder
def upload_notes_to_google_drive(drive, filename, notes):
    try:
        print("Uploading audio to Google Drive folder...")
        file = drive.CreateFile({
            "title": current_name,
            "parents": [{"id": audio_directory_id}]
        })
        file.SetContentFile(filename)
        file.Upload()
        print(f"Audio uploaded successfully! Access it here: {file['alternateLink']}")
        print("Uploading notes to Google Drive folder...")
        file = drive.CreateFile({
            "title": current_name,
            "mimeType": "text/plain",
            "parents": [{"id": note_directory_id}]
        })
        file.SetContentString(notes)
        file.Upload()
        print(f"Notes uploaded successfully! Access it here: {file['alternateLink']}")
    except Exception as e:
        print(f"Error during Google Docs upload: {e}")


if __name__ == "__main__":
    check_credentials()
    drive = authenticate_google_drive()
    record_thread = threading.Thread(target=record_audio, args=('audio_file.wav',))
    record_thread.start()
    input("Press Enter to stop recording...\n")
    recording = False
    record_thread.join()
    transcript = interpret_lecture('audio_file.wav')
    notes = synthesizing_lecture(transcript)
    upload_notes_to_google_drive(drive, 'audio_file.wav', notes)
