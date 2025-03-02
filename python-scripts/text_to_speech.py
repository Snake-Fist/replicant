import sys
import requests
import os
import json

# Force UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

# Load ElevenLabs API key from settings.json
with open("config/settings.json", "r") as f:
    config = json.load(f)
ELEVENLABS_API_KEY = config["ELEVENLABS_API_KEY"]
VOICE_ID = config["ELEVENLABS_VOICE_ID"]  # Set your preferred ElevenLabs voice ID

# Directory where responses are stored
recordings_dir = "recordings"

# Get the **latest** AI response file
response_files = [f for f in os.listdir(recordings_dir) if f.endswith("_response.txt")]

if not response_files:
    print("[ERROR] No AI response files found. Please run generate_response.py first.")
    exit()

# Sort response files by most recent modification time
latest_response = max(response_files, key=lambda f: os.path.getmtime(os.path.join(recordings_dir, f)))
input_txt = os.path.join(recordings_dir, latest_response)

def read_ai_response(file_path):
    """Read the latest AI response from the file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        print(f"[ERROR] Failed to read {file_path}: {e}")
        return None

def text_to_speech(text, output_file):
    """Send AI-generated text to ElevenLabs API to generate speech."""
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "voice_settings": {
                "stability": 0.7,
                "similarity_boost": 0.5
            }
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"[SUCCESS] Speech generated and saved to {output_file}")
            return output_file
        else:
            print(f"[ERROR] Failed to generate speech: {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] Exception while generating speech: {e}")
        return None

# Read AI response
ai_text = read_ai_response(input_txt)

if ai_text:
    print(f"[AI RESPONSE]:\n{ai_text}")

    # Convert text to speech (use matching filename)
    speech_file = input_txt.replace("_response.txt", ".mp3")
    text_to_speech(ai_text, speech_file)
else:
    print("[ERROR] Failed to read AI response.")
