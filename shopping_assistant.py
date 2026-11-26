
import speech_recognition as sr
import subprocess

from shopping_list import add_product, show_shopping_list
from intent_understanding import extract_product

recognizer = sr.Recognizer()


def speak(text):

    print("ASSISTANT:", text)
    subprocess.run(["say", text])


def listen():

    with sr.Microphone(device_index=0) as source:

        print("\nListening...")

        try:

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=10
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
            speak("Sorry, I could not understand.")
            return ""

        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            return ""


def get_yes_no():

    while True:

        answer = listen()

        if answer == "":
            continue

        words = answer.split()

        if "yes" in words:
            return "yes"

        elif "no" in words:
            return "no"

        else:
            speak("Please say yes or no.")


def start_assistant():

    speak("Welcome to your shopping assistant.")

    with sr.Microphone(device_index=0) as source:

        print("Calibrating microphone...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

    speak("Tell me the first product you want.")

    while True:

        sentence = listen()

        if sentence == "":
            continue

        # Check whether user wants to finish
        finish_words = [
            "that's it",
            "that is it",
            "finish",
            "done",
            "finish shopping",
            "stop"
        ]

        if sentence in finish_words:
            break

        product_details = extract_product(sentence)

        if product_details is None:

            speak("I could not identify the product.")

            speak("Please mention the product name clearly.")

            continue

        add_product(product_details)

        speak(
            "Added "
            + product_details["product"]
            + ". Quantity "
            + str(product_details["quantity"])
            + " "
            + product_details["unit"]
        )

        speak("Would you like to add another product?")

        answer = get_yes_no()

        if answer == "yes":

            speak("Tell me the next product.")

        else:

            break

    speak("Your shopping list is ready.")

    show_shopping_list()


if __name__ == "__main__":

    start_assistant()
