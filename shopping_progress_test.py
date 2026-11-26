
from shopping_list import (
    get_shopping_list,
    update_found_quantity,
    update_collected_quantity,
    show_shopping_list
)


# Get shopping list
shopping_list = get_shopping_list()

print("\nInitial shopping progress:")

show_shopping_list()


# Test finding two packets of Britannia biscuits
print("\nDetecting two packets...")

update_found_quantity(
    "biscuits",
    "Britannia",
    2
)


# Test collecting one packet
print("\nCollecting one packet...")

update_collected_quantity(
    "biscuits",
    "Britannia",
    1
)


# Display final progress
print("\nFinal shopping progress:")

show_shopping_list()
