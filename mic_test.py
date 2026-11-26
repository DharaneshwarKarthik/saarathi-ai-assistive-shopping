import pyaudio

audio = pyaudio.PyAudio()

print("Available audio input devices:")

for i in range(audio.get_device_count()):
    device = audio.get_device_info_by_index(i)

    if device["maxInputChannels"] > 0:
        print(i, device["name"])

audio.terminate()