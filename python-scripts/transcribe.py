import sys
import openai
import os
import json

# Force UTF-8 encoding (fixes UnicodeEncodeError on Windows)
sys.stdout.reconfigure(encoding='utf-8')

# Load API key from settings.json
with open("config/settings.json", "r") as f:
    config = json.load(f)
OPENAI_API_KEY = config["OPENAI_API_KEY"]

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Directory where WAV files are stored
recordings_dir = "recordings"

# Find the first available .wav file
wav_files = [f for f in os.listdir(recordings_dir) if f.endswith(".wav")]

if not wav_files:
    print("[ERROR] No WAV files found in recordings/. Please convert a PCM file first.")
    exit()

# Select the first available WAV file
input_wav = os.path.join(recordings_dir, wav_files[0])

def transcribe_audio(file_path):
    """Send audio file to OpenAI Whisper for transcription."""
    try:
        with open(file_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"  # Ensures plain text output
            )
            return response
    except Exception as e:
        print(f"[ERROR] Failed to transcribe {file_path}: {e}")
        return None

# Perform transcription
transcript = transcribe_audio(input_wav)

if transcript:
    print(f"[TRANSCRIPTION]:\n{transcript}")

    # Save the transcription to a text file
    transcript_file = input_wav.replace(".wav", ".txt")
    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(transcript)

    print(f"[SUCCESS] Transcription saved to {transcript_file}")
else:
    print("[ERROR] Transcription failed.")
