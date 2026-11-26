
from shopping_list import get_shopping_list


# Match YOLO detected objects with shopping list
def match_products(detected_objects):

    shopping_list = get_shopping_list()

    matched_products = []

    for item in shopping_list:

        product = item["product"].lower()

        for detected in detected_objects:

            detected = detected.lower()

            # Basic category matching
            if product in detected or detected in product:

                if item["status"] == "Pending":

                    item["status"] = "Detected"

                    matched_products.append(item)

                    break

    return matched_products


# Display shopping progress
def show_progress():

    shopping_list = get_shopping_list()

    print("\n========== SHOPPING PROGRESS ==========")

    for item in shopping_list:

        print(
            item["product"],
            "-",
            item["status"]
        )

    print("=======================================")
