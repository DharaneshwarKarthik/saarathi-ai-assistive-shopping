
from shopping_list import add_product, show_shopping_list

from product_matching import match_products, show_progress


# Add sample shopping requirements
add_product({
    "product": "milk",
    "brand": "Amul",
    "quantity": 1,
    "unit": "litre",
    "status": "Pending"
})

add_product({
    "product": "biscuits",
    "brand": "Parle-G",
    "quantity": 2,
    "unit": "packets",
    "status": "Pending"
})


# Simulated YOLO detections
detected_objects = [
    "bottle",
    "cup",
    "biscuits"
]


print("YOLO DETECTED:")

for obj in detected_objects:
    print(obj)


# Match detections
matched = match_products(detected_objects)

print("\nMATCHED PRODUCTS:")

for item in matched:
    print(item["product"], item["brand"])


# Display progress
show_progress()
