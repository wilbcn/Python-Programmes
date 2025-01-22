def control_user_choice(prompt, menu_range):
    """
    Validates user input to help navigate Menus and user sub menus throughout the programme.
    Range can be specified to neatly display user menus and error checks back to the User.
    """
    while True:
        try:
            print(f"Please choose an option from the menu. {menu_range.start}-{menu_range.stop-1}")
            user_choice = input(prompt).strip()

            # Check for empty input
            if not user_choice:
                print("Choice cannot be empty. Please choose a number")
                continue

            # Check input is numeric
            if not user_choice.isdigit():
                print("Please choose a number from the Menu.")
                continue

            # Convert user choice to an integer
            user_choice = int(user_choice)

            # Check input is within the menu range of options
            if user_choice not in menu_range:
                print(f"Please choose a valid menu option: {menu_range.start}-{menu_range.stop-1}")
                continue

            # Return the user menu choice
            return user_choice

        except ValueError:
            print("An error has occurred, please try again with a valid number.")


def retry_func(prompt=" "):
    """
    Prompts the user if they would like to continue or cancel the operation. Used in situations before
    the user can impact the system such as removing a book or a user permanently.
    The prompt argument can be utilised to provide a clearer message for the Continue option.
    """
    while True:
        try:
            print(f"1 - Continue: {prompt}")
            print("2 - Cancel")
            retry = int(input("Enter here: "))
            if retry == 1:
                return True
            elif retry == 2:
                return False
            else:
                print("Please choose either 1 or 2.")
        except ValueError:
            print("Choice cannot be empty or text. Please choose a number.")


def validate_text(item,name=" "):
    """
    Cleans and validates user text for consistency, stripping any whitespace, capitalises the first letter,
    and ensures no numeric values are present. Used in multiple .py files in our Library programme.
    Books.py - Title,Author,Publisher.
    Users.py - Firstname,Surname,Street name,Remove user by firstname.
    """

    while True:
        item = item.strip().capitalize()
        if not item:
            print(f"{name} cannot be empty.")
        elif any(char.isdigit() for char in item):
            print(f"{name} must not contain numeric values.")
        else:
            return item

        item = input("Please try again: ")
