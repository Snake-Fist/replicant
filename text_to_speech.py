import requests

ELEVENLABS_API_KEY = "YOUR_ELEVENLABS_API_KEY"
VOICE_ID = "YOUR_VOICE_ID"

def text_to_speech(text, output_file="response.mp3"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    payload = {"text": text, "voice_settings": {"stability": 0.7, "similarity_boost": 0.5}}

    response = requests.post(url, json=payload, headers=headers)
    with open(output_file, "wb") as f:
        f.write(response.content)
    return output_file
