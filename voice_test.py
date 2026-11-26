
import speech_recognition as sr

recognizer = sr.Recognizer()

microphone = sr.Microphone(device_index=0)

print("Calibrating microphone...")

with microphone as source:
    recognizer.adjust_for_ambient_noise(source, duration=1)

    print("\nSpeak something now...")

    audio = recognizer.listen(source, phrase_time_limit=8)

    print("Recognizing your voice...")

try:
    text = recognizer.recognize_google(
        audio,
        language="en-IN"
    )

    print("\nYou said:", text)

except sr.UnknownValueError:
    print("Sorry, I couldn't understand your voice.")

except sr.RequestError:
    print("Internet or speech recognition service error.")
