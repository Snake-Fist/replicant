import sys
import wave
import os

# Force UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

# Directory where PCM files are stored
recordings_dir = "recordings"

# Find the latest PCM file
pcm_files = [f for f in os.listdir(recordings_dir) if f.endswith(".pcm")]

if not pcm_files:
    print("[ERROR] No PCM files found. Please record audio first.")
    exit()

# Select the most recent PCM file
latest_pcm = max(pcm_files, key=lambda f: os.path.getmtime(os.path.join(recordings_dir, f)))
input_pcm = os.path.join(recordings_dir, latest_pcm)
output_wav = input_pcm.replace(".pcm", ".wav")

def pcm_to_wav(input_file, output_file):
    """Convert PCM audio file to WAV format with correct parameters."""
    try:
        with open(input_file, "rb") as pcm_file:
            pcm_data = pcm_file.read()

        # Create the WAV file with correct format
        with wave.open(output_file, "wb") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(48000)  # 48kHz (Discord standard)
            wav_file.writeframes(pcm_data)

        print(f"[SUCCESS] Converted {input_file} → {output_file}")

    except Exception as e:
        print(f"[ERROR] Failed to convert {input_file} to WAV: {e}")

# Perform the conversion
pcm_to_wav(input_pcm, output_wav)
