
import speech_recognition as sr
import subprocess

# Create speech recognizer
recognizer = sr.Recognizer()

# Function to speak
def speak(text):
    print("ASSISTANT:", text)
    subprocess.run(["say", text])

# Function to listen
def listen():
    with sr.Microphone() as source:

        print("\nListening...")

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

            print("Recognizing...")

            text = recognizer.recognize_google(
                audio,
                language="en-IN"
            )

            print("YOU:", text)
            return text.lower()

        except sr.WaitTimeoutError:
            return ""

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand.")
            return ""

        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            return ""


# Main program
speak("Hello! Your shopping assistant is ready.")

print("Voice assistant started.")

# Adjust microphone for background noise
with sr.Microphone() as source:
    print("Calibrating microphone...")
    recognizer.adjust_for_ambient_noise(source, duration=1)

speak("You can tell me what you need.")

while True:

    command = listen()

    if command == "":
        continue

    if "stop assistant" in command:
        speak("Goodbye. Shopping assistant stopped.")
        break

    elif "hello" in command:
        speak("Hello! How can I help you?")

    elif "what can you do" in command:
        speak("I can help you find products and assist you with shopping.")

    else:
        speak("I heard you say " + command)
