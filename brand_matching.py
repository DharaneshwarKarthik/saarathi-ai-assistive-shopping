
import re


def clean_text(text):

    text = text.lower()

    # Remove spaces, punctuation and special characters
    text = re.sub(r"[^a-z0-9]", "", text)

    return text


def check_brand(brand, ocr_text):

    clean_brand = clean_text(brand)
    clean_ocr = clean_text(ocr_text)

    if clean_brand in clean_ocr:
        return True

    return False


# Test the matching system
if __name__ == "__main__":

    brand = "Coca-Cola"

    test_texts = [
        "Coca-Cola Original Taste",
        "Coca Cola",
        "COCACOLA",
        "VIKTOR E FRANKL Search For Meaning",
        "Pepsi Original"
    ]

    print("\n========== BRAND MATCHING TEST ==========")

    for text in test_texts:

        result = check_brand(brand, text)

        print("\nOCR Text:", text)

        if result:
            print("Result: Brand match found")
        else:
            print("Result: No brand match")
