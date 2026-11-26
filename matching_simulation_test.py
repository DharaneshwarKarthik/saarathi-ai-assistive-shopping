
from shopping_list import get_shopping_list, update_product_status


# Number of consecutive frames required
REQUIRED_FRAMES = 5

# Track how many consecutive frames each product is detected
detection_counts = {}

# Remember which products have already been announced
announced_products = set()


# Possible YOLO object mappings
object_mapping = {
    "milk": ["bottle"],
    "biscuits": ["sandwich"],
    "coca-cola": ["bottle"],
    "sprite": ["bottle"],
    "curd": ["bowl"],
    "cake": ["cake"],
    "rice": ["bowl"],
    "bread": ["sandwich"],
    "sugar": ["bowl"],
    "oil": ["bottle"],
    "water": ["bottle"],
    "chips": ["packet"]
}


def check_detections(detected_objects):

    shopping_list = get_shopping_list()

    for item in shopping_list:

        product = item["product"]
        brand = item["brand"]

        if item["status"] != "Pending":
            continue

        possible_objects = object_mapping.get(product, [product])

        found = False

        for detected in detected_objects:
            if detected in possible_objects:
                found = True
                break

        if found:

            if product not in detection_counts:
                detection_counts[product] = 0

            detection_counts[product] += 1

            print(
                product,
                "- Detection count:",
                detection_counts[product]
            )

            if (detection_counts[product] >= REQUIRED_FRAMES
                    and product not in announced_products):

                print("\nASSISTANT: Possible match for", product,
                      "detected.")

                update_product_status(
                    product,
                    brand,
                    "Possible match"
                )

                announced_products.add(product)

        else:
            detection_counts[product] = 0


# Simulated camera detections
simulated_frames = [
    ["person", "bottle"],
    ["person", "bottle"],
    ["person", "bottle"],
    ["person", "bottle"],
    ["person", "bottle"],
    ["person"],
    ["person", "sandwich"],
    ["person", "sandwich"],
    ["person", "sandwich"],
    ["person", "sandwich"],
    ["person", "sandwich"]
]


print("\n========== STABILITY TEST ==========")

for frame_number, detected_objects in enumerate(simulated_frames):

    print("\nFrame:", frame_number + 1)
    print("YOLO detected:", detected_objects)

    check_detections(detected_objects)


print("\n========== FINAL SHOPPING LIST ==========")

for item in get_shopping_list():
    print(item["product"], "-", item["status"])

print("\nSimulation completed.")
