
import re


# Convert number words into numbers
number_words = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10
}


# Known product patterns and their brands
product_brands = {
    "milk": ["amul", "aavin", "heritage"],
    "biscuits": ["parle-g", "britannia", "oreo"],
    "coca-cola": ["coca-cola", "coca cola"],
    "rice": [],
    "bread": ["britannia", "modern"],
    "sugar": [],
    "oil": ["fortune", "sunflower"]
}


def convert_number(text):

    words = text.split()

    for word in words:
        if word in number_words:
            return number_words[word]

    # Look for a numeric quantity
    for word in words:
        if word.isdigit():
            return int(word)

    return 1


def extract_quantity_unit(text):

    quantity = convert_number(text)

    unit = "pieces"

    if "litre" in text or "liter" in text:
        unit = "litre"

    elif "ml" in text:
        unit = "ml"

    elif "kilogram" in text or "kg" in text:
        unit = "kg"

    elif "gram" in text or "grams" in text or "g " in text:
        unit = "grams"

    elif "packet" in text or "packets" in text:
        unit = "packets"

    elif "bottle" in text or "bottles" in text:
        unit = "bottles"

    return quantity, unit


def extract_product(text):

    text = text.lower().strip()

    brand = "Unknown"
    product = None

    # Identify the product
    for item in product_brands:

        if item in text:
            product = item
            break

    if product is None:
        return None

    # Identify the brand
    for item in product_brands[product]:

        if item in text:
            brand = item.title()
            break

    quantity, unit = extract_quantity_unit(text)

    return {
        "product": product,
        "brand": brand,
        "quantity": quantity,
        "unit": unit,
        "status": "Pending"
    }
