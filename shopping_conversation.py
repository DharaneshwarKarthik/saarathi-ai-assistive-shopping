
from shopping_assistant import listen, speak

from shopping_list import (
    get_shopping_list,
    show_shopping_list,
    update_collected_quantity,
    save_shopping_list,
    update_remaining_quantity
)


previous_response = ""


def remember_and_speak(message):

    global previous_response

    previous_response = message

    speak(message)


# Convert spoken numbers
def extract_quantity(text):

    number_words = {
        "one": 1,
        "two": 2,
        "to": 2,
        "too": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10
    }

    words = text.split()

    for word in words:

        if word in number_words:
            return number_words[word]

        if word.isdigit():
            return int(word)

    return 0


# Find product in shopping list
def find_product(text):

    shopping_list = get_shopping_list()

    for item in shopping_list:

        product = item["product"].lower()
        brand = item["brand"].lower()

        product_variations = [
            product,
            product.rstrip("s"),
            brand
        ]

        for variation in product_variations:

            if variation in text:

                return item

    return None


# Read remaining products
def read_remaining():

    shopping_list = get_shopping_list()

    remaining_items = []

    for item in shopping_list:

        quantity = item["remaining_quantity"]

        if quantity > 0:

            remaining_items.append(
                str(quantity) + " " +
                item["unit"] + " of " +
                item["brand"] + " " +
                item["product"]
            )

    if len(remaining_items) == 0:

        remember_and_speak(
            "You have completed your shopping list."
        )

        return

    message = "You still need "

    for i in range(len(remaining_items)):

        message += remaining_items[i]

        if i < len(remaining_items) - 1:
            message += ", "

    remember_and_speak(message)


# Read collected quantity
def read_collected(product_name):

    shopping_list = get_shopping_list()

    for item in shopping_list:

        if product_name in item["product"]:

            message = (
                "You have collected "
                + str(item["collected_quantity"])
                + " out of "
                + str(item["requested_quantity"])
                + " "
                + item["unit"]
            )

            remember_and_speak(message)

            return

    remember_and_speak(
        "Product not found in your shopping list."
    )


# Collect products
def collect_product(text):

    item = find_product(text)

    if item is None:

        remember_and_speak(
            "I could not identify that product."
        )

        return

    # Handle collecting everything remaining
    if "all" in text:

        quantity = item["remaining_quantity"]

    else:

        quantity = extract_quantity(text)

    if quantity <= 0:

        remember_and_speak(
            "Please tell me how many you collected."
        )

        return

    update_collected_quantity(
        item["product"],
        item["brand"],
        quantity
    )

    message = (
        "Updated. You have collected "
        + str(item["collected_quantity"])
        + " out of "
        + str(item["requested_quantity"])
        + " "
        + item["unit"]
        + ". "
        + str(item["remaining_quantity"])
        + " remaining."
    )

    remember_and_speak(message)


# Reduce requested quantity
def reduce_quantity(text):

    item = find_product(text)

    if item is None:

        remember_and_speak(
            "I could not identify the product."
        )

        return

    # Reduce by the amount the user no longer needs
    quantity = extract_quantity(text)

    if quantity == 0:

        quantity = item["remaining_quantity"]

    new_requested = (
        item["requested_quantity"] - quantity
    )

    if new_requested < item["collected_quantity"]:

        new_requested = item["collected_quantity"]

    item["requested_quantity"] = new_requested

    item["remaining_quantity"] = (
        new_requested - item["collected_quantity"]
    )

    update_remaining_quantity(item)

    save_shopping_list()

    remember_and_speak(
        "Updated your shopping requirement. "
        + str(item["remaining_quantity"])
        + " "
        + item["unit"]
        + " remaining."
    )


# Main conversation
def start_conversation():

    global previous_response

    remember_and_speak(
        "Shopping conversation started."
    )

    while True:

        command = listen()

        if command == "":
            continue

        command = command.lower()

        print("\nCOMMAND:", command)

        # Stop commands
        if (
            command == "stop"
            or "stop shopping" in command
            or "goodbye" in command
            or "exit" in command
        ):

            remember_and_speak(
                "Shopping session ended."
            )

            break

        # Repeat
        elif "repeat" in command:

            if previous_response != "":
                speak(previous_response)

        # Show shopping list
        elif (
            "shopping list" in command
            or "show my list" in command
        ):

            show_shopping_list()

            remember_and_speak(
                "I have displayed your shopping list."
            )

        # Remaining products
        elif (
            "remaining" in command
            or "left" in command
        ):

            read_remaining()

        # Reduce requirement
        elif (
            "don't need" in command
            or "do not need" in command
            or "not need" in command
        ):

            reduce_quantity(command)

        # Collection commands
        elif (
            "collected" in command
            or "picked up" in command
        ):

            collect_product(command)

        else:

            remember_and_speak(
                "Sorry, I did not understand that command."
            )


if __name__ == "__main__":

    start_conversation()
