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

# Directory where transcriptions are stored
recordings_dir = "recordings"

# Find the latest transcription file
txt_files = [f for f in os.listdir(recordings_dir) if f.endswith(".txt") and not f.endswith("_response.txt")]

if not txt_files:
    print("[ERROR] No transcriptions found. Please run transcribe.py first.")
    exit()

# Select the most recent transcription file
latest_transcription = max(txt_files, key=lambda f: os.path.getmtime(os.path.join(recordings_dir, f)))
input_txt = os.path.join(recordings_dir, latest_transcription)

def read_transcription(file_path):
    """Read the transcribed text from file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        print(f"[ERROR] Failed to read {file_path}: {e}")
        return None

def generate_response(user_input):
    """Send transcribed text to ChatGPT and return the AI response."""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERROR] Failed to generate response: {e}")
        return None

# Read transcription
transcribed_text = read_transcription(input_txt)

if transcribed_text:
    print(f"[TRANSCRIPTION]:\n{transcribed_text}")

    # Generate AI response
    ai_response = generate_response(transcribed_text)

    if ai_response:
        print(f"[AI RESPONSE]:\n{ai_response}")

        # Save AI response to a file
        response_file = input_txt.replace(".txt", "_response.txt")
        with open(response_file, "w", encoding="utf-8") as f:
            f.write(ai_response)

        print(f"[SUCCESS] Response saved to {response_file}")
    else:
        print("[ERROR] Failed to generate AI response.")
else:
    print("[ERROR] Failed to read transcription.")
