import wave

def pcm_to_wav(input_file, output_file):
    with open(input_file, "rb") as pcm_file:
        pcm_data = pcm_file.read()

    with wave.open(output_file, "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(48000)
        wav_file.writeframes(pcm_data)

    return output_file
