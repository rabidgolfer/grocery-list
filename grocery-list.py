import shelve
from datetime import date, timedelta
import os

# Define filenames for the shelves
FRUIT_SHELF_FILENAME = 'fruit_shelf'
OTHER_SHELF_FILENAME = 'grocery_shelf'


def create_or_open_shelves():
    """Creates or opens the fruit and other item shelves."""
    return (shelve.open(FRUIT_SHELF_FILENAME, writeback=True),
            shelve.open(OTHER_SHELF_FILENAME, writeback=True))


def create_grocery_list(fruit_shelf, other_shelf):
    """Populates the grocery shelves with initial items."""

    # Fruit Shelf Items
    fruit_shelf['apples'] = {'quantity': 5, 'expiry_date': date.today() + timedelta(days=7), 'fruit': True}
    fruit_shelf['bananas'] = {'quantity': 4, 'expiry_date': date.today() + timedelta(days=3), 'fruit': True}
    fruit_shelf['oranges'] = {'quantity': 6, 'expiry_date': date.today() + timedelta(days=10), 'fruit': True}

    # Other Shelf Items
    other_shelf['bread'] = {'quantity': 2, 'expiry_date': date.today() + timedelta(days=4), 'fruit': False}
    other_shelf['milk'] = {'quantity': 1, 'expiry_date': date.today() + timedelta(days=3), 'fruit': False}
    other_shelf['eggs'] = {'quantity': 12, 'expiry_date': date.today() + timedelta(days=30), 'fruit': False}


def select_shelf(shelf_choice):
    """Selects the appropriate shelf based on user input."""
    while True:
        shelf_choice = input("Select shelf (fruit or other): ").lower()
        if shelf_choice in ("fruit", "other"):
            return fruit_shelf if shelf_choice == "fruit" else other_shelf
        else:
            print("Invalid choice. Please enter 'fruit' or 'other'.")


def handle_view_command():
    """Handles the 'view' command, including input validation and shelf choices."""
    view_choice = get_view_choice()
    if view_choice:  # Valid choice
        for shelf_type in view_choice:  # Handle multiple choices ('all')
            shelf = fruit_shelf if shelf_type == "Fruit" else other_shelf
            view_grocery_list(shelf_type, shelf)


def get_view_choice():
    while True:
        choice = input("\nWhich shelf would you like to view? Enter 'fruit', 'other', or 'all': ").lower()
        if choice in ("fruit", "other"):
            return choice.capitalize()  # Return only the shelf choice
        elif choice == "all":
            return "Fruit", "Other"
        else:
            print("Invalid choice. Please enter 'fruit', 'other', or 'all'.")


def view_grocery_list(shelf_type, shelf):
    """Prints the grocery list for a specific shelf."""
    print(f"\n--- {shelf_type} Shelf ---")  # Print shelf type

    if shelf:  # Check if shelf has items
        for item, item_data in shelf.items():
            print(f"- {item_data['quantity']} {item} (Expires: {item_data['expiry_date'].strftime('%Y-%m-%d')}, Fruit: {item_data['fruit']})")
    else:
        print("This shelf is empty.")


def get_item_quantity(shelf):
    """Retrieves the quantity, expiry date, and fruit status of a specific item."""
    while True:  # Keep asking until valid input
        item_name = input("Enter item name: ")
        if item_name:
            item_data = shelf.get(item_name, {})  # Get item data, return empty dict if not found
            if item_data:  # Check if the item was found
                # Format the expiry date nicely
                expiry_date_str = item_data['expiry_date'].strftime("%Y-%m-%d")

                # Print all properties of the item
                print(f"Item: {item_name}")
                print(f"- Quantity: {item_data['quantity']}")
                print(f"- Expires: {expiry_date_str}")
                print(f"- Fruit: {item_data['fruit']}")
                return item_data  # Return the item data for potential further use
            else:
                print("Item not found.")
                return None  # Explicitly return None for clarity
        else:
            print("Item name cannot be empty.")


def update_item_quantity(shelf):
    """Updates the quantity of an existing item.
    Offers options to update, add, or reduce quantity.
    """

    item_name = input("Enter item name: ")

    if item_name not in shelf:  # Item not found case
        print(f"Item '{item_name}' not found on the shelf.")
        return  # Exit early

    current_quantity = shelf[item_name]['quantity']

    while True:
        try:
            option = int(input(f"Select an option for '{item_name}' (current quantity: {current_quantity}):\n"
                               "1. Update quantity\n"
                               "2. Add to quantity\n"
                               "3. Reduce quantity\n"
                               "Enter option: "))

            if 1 <= option <= 3:
                break  # Valid option selected
            else:
                print("Invalid option. Please choose 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number (1, 2, or 3).")

    if option == 1:
        # Update quantity
        new_quantity = int(input("Enter new quantity: "))
        shelf[item_name]['quantity'] = new_quantity
        print(f"Updated quantity of '{item_name}' to {new_quantity}.")
        if new_quantity == 0:
            del shelf[item_name]
            print(f"Removed {item_name} from the shelf.")
    elif option == 2:
        # Add to quantity
        add_quantity = int(input("Enter quantity to add: "))
        shelf[item_name]['quantity'] += add_quantity
        print(f"Added {add_quantity} to '{item_name}', new quantity is {shelf[item_name]['quantity']}.")
    else:
        # Reduce quantity
        reduce_quantity = int(input("Enter quantity to reduce: "))
        if reduce_quantity > current_quantity:
            print("Cannot reduce quantity below 0. Please try again.")
        else:
            shelf[item_name]['quantity'] -= reduce_quantity
            if shelf[item_name]['quantity'] == 0:
                del shelf[item_name]
                print(f"Removed {item_name} from the shelf.")
            else:
                print(
                    f"Reduced quantity of '{item_name}' by {reduce_quantity}, new quantity is {shelf[item_name]['quantity']}.")


def add_new_item(shelf):
    """Adds a new item to the shelf with an expiry date."""
    item_name = input("Enter item name: ")
    quantity = int(input("Enter quantity: "))

    if quantity > 0:
        while True:
            expiry_date_str = input("Enter expiry date (YYYY-MM-DD): ")
            try:
                expiry_date = date.fromisoformat(expiry_date_str)
                if expiry_date > date.today():
                    fruit_str = input(f"Is {item_name} a fruit (Yes/No)? ").lower()

                    # Check for valid input
                    if fruit_str in ("yes", "y", "true", "t"):
                        fruit = True
                    elif fruit_str in ("no", "n", "false", "f"):
                        fruit = False
                    else:
                        print("Invalid input. Please answer with 'Yes' or 'No'.")
                        continue  # Ask again for valid input

                    shelf[item_name] = {'quantity': quantity, 'expiry_date': expiry_date, 'fruit': fruit}
                    break
                else:
                    print("Expiry date must be later than today.")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
    else:
        print("Quantity cannot be negative or zero.")


def delete_shelf(shelf):
    """Deletes the entire grocery shelf and its data file."""
    confirmation = input("Are you sure you want to delete the entire grocery shelf? (Yes/No): ").lower()
    if confirmation in ("yes", "y"):
        shelf.close()  # Close the shelf before deleting
        os.remove("grocery_shelf.db")  # Delete the shelf data file
        print("Grocery shelf deleted successfully.")
    else:
        print("Deletion canceled.")


def clean_shelf(shelf):
    """Cleans the grocery shelf by removing items based on user's choice."""
    while True:
        clean_choice = input("Clean only fruit items (f) or clean all items (a)? Enter f or a: ").lower()

        if clean_choice == "f":
            to_remove = [item for item, data in shelf.items() if data['fruit']]
        elif clean_choice == "a":
            to_remove = list(shelf.keys())  # Get a copy of keys for safe removal
        else:
            print("Invalid choice. Please enter 'f' or 'a'.")
            continue

        for item in to_remove:
            del shelf[item]

        print("Grocery shelf cleaned successfully.")
        break


def main():
    # Open both shelves
    fruit_shelf, other_shelf = create_or_open_shelves()

    # Call create_grocery_list if both shelves are empty (first time running)
    if not fruit_shelf and not other_shelf:  # Check if both are empty
        create_grocery_list(fruit_shelf, other_shelf)  # Add items to both shelves

    while True:
        command = input("Enter a command (view, add, update, get, delete, clean, quit): ").lower()
        if command == "view":
            handle_view_command()
        elif command == "add":
            add_new_item(shelf)
        elif command == "update":
            update_item_quantity(shelf)
        elif command == "get":
            get_item_quantity(shelf)  # Get item data (which is a dictionary)
        elif command == "delete":
            delete_shelf(shelf)
        elif command == "clean":
            clean_shelf(shelf)
        elif command == "quit":
            break
        else:
            print("Invalid command. Please try again.")

    fruit_shelf.close()
    other_shelf.close()  # Close both shelves


if __name__ == "__main__":
    main()
