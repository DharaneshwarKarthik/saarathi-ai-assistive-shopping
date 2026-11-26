
import json
import os

FILE_NAME = "shopping_data.json"

shopping_list = []


# Load shopping list
def load_shopping_list():

    global shopping_list

    if os.path.exists(FILE_NAME):

        with open(FILE_NAME, "r") as file:
            shopping_list = json.load(file)

        # Upgrade older shopping-list entries
        for item in shopping_list:

            if "requested_quantity" not in item:
                item["requested_quantity"] = item.get("quantity", 1)

            if "found_quantity" not in item:
                item["found_quantity"] = 0

            if "collected_quantity" not in item:
                item["collected_quantity"] = 0

            if "remaining_quantity" not in item:
                item["remaining_quantity"] = item["requested_quantity"]

            if "status" not in item:
                item["status"] = "Pending"

        save_shopping_list()

    else:
        shopping_list = []


# Save shopping list
def save_shopping_list():

    with open(FILE_NAME, "w") as file:
        json.dump(shopping_list, file, indent=4)


# Add a new product
def add_product(product_details):

    product = product_details.copy()

    product["requested_quantity"] = product.get(
        "quantity", 1
    )

    product["found_quantity"] = 0
    product["collected_quantity"] = 0

    product["remaining_quantity"] = product["requested_quantity"]

    product["status"] = "Pending"

    shopping_list.append(product)

    save_shopping_list()


# Display shopping list
def show_shopping_list():

    print("\n========== YOUR SHOPPING LIST ==========")

    if len(shopping_list) == 0:

        print("Your shopping list is empty.")

    for item in shopping_list:

        print("\nProduct:", item["product"])
        print("Brand:", item["brand"])

        print(
            "Requested quantity:",
            item["requested_quantity"]
        )

        print(
            "Found quantity:",
            item["found_quantity"]
        )

        print(
            "Collected quantity:",
            item["collected_quantity"]
        )

        print(
            "Remaining quantity:",
            item["remaining_quantity"]
        )

        print("Unit:", item["unit"])
        print("Status:", item["status"])

        print("----------------------------------------")


# Return shopping list
def get_shopping_list():

    return shopping_list


# Update product status
def update_status(product_name, new_status):

    for item in shopping_list:

        if item["product"] == product_name:

            item["status"] = new_status

    save_shopping_list()


# Update product status using product and brand
def update_product_status(product_name, brand, new_status):

    for item in shopping_list:

        if (item["product"] == product_name
                and item["brand"] == brand):

            item["status"] = new_status

            save_shopping_list()

            return True

    return False


# Update detected quantity
def update_found_quantity(product_name, brand, quantity):

    for item in shopping_list:

        if (item["product"] == product_name
                and item["brand"] == brand):

            item["found_quantity"] += quantity

            if item["found_quantity"] > item["requested_quantity"]:
                item["found_quantity"] = item["requested_quantity"]

            update_remaining_quantity(item)

            save_shopping_list()

            return True

    return False


# Update collected quantity
def update_collected_quantity(product_name, brand, quantity):

    for item in shopping_list:

        if (item["product"] == product_name
                and item["brand"] == brand):

            item["collected_quantity"] += quantity

            if item["collected_quantity"] > item["requested_quantity"]:
                item["collected_quantity"] = item["requested_quantity"]

            update_remaining_quantity(item)

            save_shopping_list()

            return True

    return False


# Calculate remaining quantity and status
def update_remaining_quantity(item):

    item["remaining_quantity"] = (
        item["requested_quantity"]
        - item["collected_quantity"]
    )

    if item["collected_quantity"] >= item["requested_quantity"]:

        item["status"] = "Completed"

    elif item["collected_quantity"] > 0:

        item["status"] = "Partially completed"

    elif item["found_quantity"] > 0:

        item["status"] = "Possible match"

    else:

        item["status"] = "Pending"


# Load saved shopping list when program starts
load_shopping_list()
