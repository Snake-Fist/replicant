import openai

API_KEY = "YOUR_OPENAI_API_KEY"

def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        response = openai.Audio.transcribe("whisper-1", audio_file)
        return response["text"]

transcription = transcribe_audio("audio.wav")
print("Transcription:", transcription)
