import re
from datetime import datetime
from utils import control_user_choice
from utils import retry_func
from utils import validate_text


class Users:
    """
    Represents a single user in the Library System. Contains the following attributes:

    Username: Unique identifier for each user
    Firstname: The firstname of the user
    Surname: The surname of the user
    House Number: The house number of the user as a numeric value
    Street Name: The street name of the user
    Postcode: The postcode of the user, validated using regex
    Email Address: The email address of the user, validated using regex
    Date of Birth: The date of birth of the user, utilises datetime module for valid dob.

    Leverages methods from utils.py to clean and validate user input, and safely navigate sub menus.

    Contains methods to:
    - Retrieve user attributes i.e. return_username
    - Edit each user attribute
    - String representation method for cleanly display
    """

    def __init__(self, username, firstname, surname, house_number, street_name, postcode, email_address, date_of_birth):

        self.username = username
        self.firstname = firstname
        self.surname = surname
        self.house_number = house_number
        self.street_name = street_name
        self.postcode = postcode
        self.email_address = email_address
        self.date_of_birth = date_of_birth

    def __str__(self):
        """Returns the string representation of our user's usernames"""
        return self.username

    def return_username(self):
        """Returns the username of the User object"""
        return self.username

    def return_firstname(self):
        """Returns the firstname of the User object"""
        return self.firstname

    def return_surname(self):
        """Returns the surname of the User object"""
        return self.surname

    def return_house_number(self):
        """Returns the house number of the User object"""
        return self.house_number

    def return_street_name(self):
        """Returns the street name of the User object"""
        return self.street_name

    def return_postcode(self):
        """Returns the postcode of the User object"""
        return self.postcode

    def return_email(self):
        """Returns the email address of the User object"""
        return self.email_address

    def return_dob(self):
        """Returns the date of birth of the User object"""
        return self.date_of_birth

    def edit_firstname(self, new_firstname):
        """Takes user input to edit a users firstname"""
        self.firstname = new_firstname
        print(f"Firstname was updated to '{new_firstname}'")
        print("Returning to Edit Menu")

    def edit_surname(self, new_surname):
        """Takes user input to edit a users surname"""
        self.surname = new_surname
        print(f"Surname was updated to '{new_surname}'")
        print("Returning to Edit Menu")

    def edit_email_address(self, new_email):
        """Takes user input to edit a users email address"""
        self.email_address = new_email
        print(f"Email address was updated to '{new_email}'")
        print("Returning to Edit Menu")

    def edit_dob(self, new_dob):
        """Takes user input to edit a users date of birth"""
        self.date_of_birth = new_dob
        print(f"Date of birth was updated to '{new_dob}'")
        print("Returning to Edit Menu")


class UserList:
    """
    Stores and organises our collection of Users in the library system.
    This class provides multiple functionalities, including:
    - Add a new user
    - Remove a user
    - Edit user attributes
    - Count total users
    - Display user information
    - Save users in a dictionary for easy lookup

    - users_dict (dict) stores our users objects, using a users username as its key.

    - Leverages retry_func from utils.py, which provides the user the choice to retry whatever
      process they were performing. i.e. title was not found, retry.
    """

    def __init__(self):
        self.users_dict = {}

    def save_user(self, username, new_user):
        """Saves a user to the user dictionary using a users username as the key."""
        self.users_dict[username] = new_user

    def set_username(self):
        """
        Takes user input to set the username of the new user. Ensures no duplicate usernames by checking the
        user dictionary, usernames are between 6-15 characters, and no empty strings.
        """
        print("Please write the username for this new user. Username must contain 6-15 characters.")
        while True:
            username = input("Username: ").strip().capitalize()
            if not username:
                print("Username must not be empty. Try again.")
            elif not (6 <= len(username) <= 15):
                print("Username must be between 6 and 15 characters. Please try again.")
            elif username in self.users_dict:
                print(f"Username: {username} is already taken. Please try another username.")
            else:
                print("Username accepted.")
                return username

    def set_firstname(self, new_user):
        """
        Takes user input to set the firstname of the user. Utilises validate_text to ensure the returned
        firstname has been properly validated. Uses new_user as a boolean to indicate whether logic is for
        a new user or existing one.
        """
        if new_user:
            print("Please write the firstname for this new user.")

        elif not new_user:
            print("Please write the new first name to update this user.")

        while True:
            firstname = input("Firstname: ")
            validate_firstname = validate_text(firstname, "Firstname")
            print("Firstname accepted.")
            return validate_firstname

    def set_surname(self, new_user):
        """
        Takes user input to set the surname of the user. Utilises validate_text to ensure the returned
        surname has been properly validated. Uses new_user as a boolean to indicate whether logic is for
        a new user or existing one.
        """
        if new_user:
            print("Please write the surname for this new user.")

        elif not new_user:
            print("Please write the new surname to update this user.")

        while True:
            surname = input("Surname: ")
            validate_surname = validate_text(surname, "Surname")
            print("Surname accepted.")
            return validate_surname

    def set_house_number(self):
        """
        Takes user input to set the house number of the new user. Accepts numbers only.
        Does not allow unrealistic lengths or empty inputs.
        """
        print("Please write the house number of the new users address")
        while True:
            try:
                house_number = (input("House number: ")).strip()

                if not house_number:
                    print("House number cannot be empty. Please try again.")
                elif not house_number.isdigit():
                    print("House number can only contain numeric values. Please try again.")
                elif house_number == '0' or len(house_number) > 4:
                    print("House number cannot be 0 or greater than 4 digits.")
                else:
                    print("House number accepted.")
                    return int(house_number)

            except ValueError:
                print("House number should contain positive numeric values only. E.g. 19")

    def set_street_name(self):
        """
        Takes user input to set the street name of the user. Utilises validate_text to ensure the returned
        street name has been properly validated.
        """
        print("Please write the street name for this new user.")
        street_name = input("Street name: ")
        validate_street_name = validate_text(street_name, "Street name")
        print("Street name accepted.")
        return validate_street_name.title()

    def set_postcode(self):
        """
        Takes user input to set the postcode of the new user. Uses the re module to validate
        the input using UK postcode format.
        """

        # Regex pattern for UK postcodes
        postcode_format = r"^[A-Z]{1,2}[0-9][A-Z0-9]?\s?[0-9][A-Z]{2}$"

        print("Please write a valid UK postcode for this new user")

        while True:
            print("Example postcode: SW1A 1AA")
            postcode = input("Postcode: ").strip()

            # Validate the postcode
            if not postcode:
                print("Postcode cannot be empty. Please try again.")
                continue

            if re.match(postcode_format, postcode.upper()):
                # Adds a space inbetween each section to normalise the format if missing.
                if " " not in postcode:
                    postcode = postcode[:-3] + " " + postcode[-3:]
                print("Postcode accepted.")
                return postcode.upper()
            else:
                print("Invalid postcode. Please try again using correct UK postcode format.")

    def set_email(self, new_user):
        """
        Takes user input to set the surname of the user. Utilises validate_text to ensure the returned
        surname has been properly validated. Uses new_user as a boolean to indicate whether logic is for
        a new user or existing one.
        Uses regex to set a valid email address by specifying a valid pattern.
        """

        # Regex pattern for valid email address
        email_format = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if new_user:
            print("Please write a valid email address for this new user. E.g. johnsmith@gmail.com")

        elif not new_user:
            print("Please write a new email address to update this user.")

        while True:
            email_address = input("Email address: ").strip()

            if not email_address:
                print("Input cannot be empty. Please try again.")
                continue

            if re.match(email_format, email_address):
                print("Email address accepted.")
                return email_address.lower()
            else:
                print("Invalid email address format. Please try again")

    def set_dob(self, new_user):
        """
        Takes user input to set the date of birth of the new user. Uses datetime module to validate
        the input. Uses new_user as a boolean to indicate whether logic is for
        a new user or existing one.
        """
        while True:
            try:
                if new_user:
                    print("Please write the date of birth for the new user, including"
                          " the dashes. (YYYY-MM-DD).")

                elif not new_user:
                    print("Please write the new date of birth to update this user.")
                    print("(YYYY-MM-DD). Make sure to include the dashes.")

                dob = input("User date of birth: ").strip()

                if not dob:
                    print("Input cannot be empty. Please try again.")
                    continue

                # Parse the initial dob string.
                validate_dob = datetime.strptime(dob, "%Y-%m-%d").date()

                # Validate new user dob.
                if validate_dob >= datetime.now().date():
                    print("The date of birth entered cannot be in the future. Please try again.")
                elif (datetime.now().year - validate_dob.year) > 110:
                    print("Year is too far below the current year. Please try again")
                else:
                    print("Date of birth accepted.")
                    return validate_dob

            except ValueError:
                print("Invalid format, please try again.")

    def add_new_user(self):
        """
        This method creates a new user to use the Library System and saves them to our users dictionary.
        (new_user=True) - Boolean values are used as arguments in the method calls as the setter methods
        are utilised elsewhere in order to edit user attributes.

        When all setter methods have been called, we use the save_user method to add this user to our dictionary,
        with the users username as the key.
        """

        username = self.set_username()
        firstname = self.set_firstname(new_user=True)
        surname = self.set_surname(new_user=True)
        house_number = self.set_house_number()
        street_name = self.set_street_name()
        postcode = self.set_postcode()
        email = self.set_email(new_user=True)
        date_of_birth = self.set_dob(new_user=True)

        # Create and save the user
        new_user = Users(username, firstname, surname, house_number, street_name, postcode, email, date_of_birth)
        print(f"A new user: '{new_user.username}' was successfully added to the system.")
        self.save_user(new_user.username, new_user)

    def remove_single_user(self, matching_users):
        """
        Removes a single user from the Users dictionary. Accepts one argument matching_users, which is passed
        to this method via remove_user_main. matching_users is a tuple and its purpose is to ensure a single
        user is removed in the event of two users who share the same first name.

        Removes the specified user from users_dict and provides safety check which prompts the user if they
        really want to remove this user: retry_func
        """

        # Unpack the Tuple
        username, user_attribute = matching_users

        print(f"User: {user_attribute.firstname} {user_attribute.surname}.")
        print("Would you like to proceed to remove this user?")
        if retry_func("Remove user"):
            del self.users_dict[username]
            print(f"{user_attribute.firstname} {user_attribute.surname} has been removed from the system.")
            print("Returning to User Menu")
            return

        else:
            print("Returning to User Menu")
            return

    def remove_user_main(self):
        """
        Takes user input and passes a single user to remove to remove_single_user method. Utilises validate_text
        from utils to cleanly validate user input. Contains logic to catch multiple users who share the same firstname.
        In the event of multiple match cases, the user is informed and is able to select just one user
        based on the index position of the match cases that have been added to a list: matched_users.
        """

        if not self.users_dict:
            print("There are no users to remove")
            return

        while True:
            print("Type the firstname of the user you wish to remove from the system.")
            user_to_remove = input("Enter here: ")
            user_to_remove = validate_text(user_to_remove, "Firstname")

            matching_users = []

            # Find all users that match the provided input
            for username, user_attribute in self.users_dict.items():
                if user_attribute.firstname == user_to_remove:
                    matching_users.append((username, user_attribute))

            if not matching_users:
                print(f"No users were found with firstname: {user_to_remove}")
                if not retry_func("Retry search"):
                    print("Returning to User Menu")
                    return
            # Single firstname match case
            elif len(matching_users) == 1:
                print("One user found.")
                self.remove_single_user(matching_users[0])  # Pass a single tuple
                return

            # Handle multiple firstname match cases
            else:
                print(f"There are {len(matching_users)} user(s) with the firstname {user_to_remove}")
                for index, (username, user_attribute) in enumerate(matching_users, start=1):
                    print(f"{index} - Username: {username}, Full Name: "
                          f"{user_attribute.firstname} {user_attribute.surname}")

                # Get the index position from the user for user to remove
                try:
                    print("Please specify the user to remove by its number position. E.g. 1")
                    user_index = int(input("Enter here: ")) - 1
                    if 0 <= user_index < len(matching_users):
                        self.remove_single_user(matching_users[user_index])
                        return

                    else:
                        print(f"There is no user for that number. Please choose a number between 1"
                              f" and {len(matching_users)}")

                except ValueError:
                    print("Invalid Input. Please enter a number that corresponds to a question.")

    def count_total_users(self):
        """
        Displays to the user how many users there are in total in the Library System by counting
        the length of the users_dict.
        """
        if not self.users_dict:
            print("There are currently 0 users in the Library system database.")
        elif len(self.users_dict) == 1:
            print("There is currently 1 user in the Library system database.")
        else:
            print(f"There are currently {len(self.users_dict)} users in the Library System database.")

    def lookup_username(self):
        """
        Takes user input and returns a user object with the username as its key. Used in other method calls
        where the user is searching for a specific user via their username. Contains checks to ensure
        users exist in the library system.
        """
        if not self.users_dict:
            print("There are no users in the Library system database.")
            return False

        while True:
            print("Please enter the username of the user")

            # Validate_text is not called as usernames may contain numbers
            username_to_find = input("Enter here: ").strip().capitalize()

            if not username_to_find:
                print("Username cannot be empty")
                continue

            if username_to_find in self.users_dict:
                user = self.users_dict[username_to_find]
                return user
            else:
                print(f"No user found with username: {username_to_find}")
                if not retry_func("Retry search"):
                    print("Returning to User Menu")
                    return

    def display_user_info(self):
        """
        Displays all information on record about a specific user. Calls lookup_username to get the user username.
        Calls the return methods from our User class for easy information retrieval.
        """

        user = self.lookup_username()

        if not user or not isinstance(user, Users):
            print("Returning to Users Menu")
            return

        print(f"Displaying information for user: {user}")
        print(f"Username: {user.return_username()}")
        print(f"Firstname: {user.return_firstname()}")
        print(f"Surname: {user.return_surname()}")
        print(f"House number: {user.return_house_number()}")
        print(f"Street name: {user.return_street_name()}")
        print(f"Postcode: {user.return_postcode()}")
        print(f"Email address: {user.return_email()}")
        print(f"Date of birth: {user.return_dob()}")
        return

    def edit_user_menu(self):
        """
        Provides an additional menu for the User to edit Library user attributes. Contains method calls for the
        to edit a variety of user attributes.

        Utilises control_user_choice for clean and safe menu navigation.
        Reuses the setter methods for code re-usability, inserting (new_user=False) as a boolean to follow
        the appropriate code logic.
        """
        if not self.users_dict:
            print("There are no users to edit")
            return

        username = self.lookup_username()

        if not username or not isinstance(username, Users):
            return

        print(f"Displaying editor menu for Username: {username}")
        while True:
            print("\n--- Library System User Editor Menu ---")
            print("Choose an option from the Sub Menu")
            print("1 - Edit Firstname")
            print("2 - Edit Surname")
            print("3 - Edit Email Address")
            print("4 - Edit Date of Birth")
            print("5 - Exit edit menu")

            # Gets the users choice and ensures valid input by calling control_user_choice from utils.py
            user_choice = control_user_choice("Enter here: ", range(1, 6))

            # Takes the user to the appropriate sub menu or quits the programme
            if user_choice == 1:
                print(f"Username: {username} has current firstname '{username.firstname}'")
                new_firstname = self.set_firstname(new_user=False)
                username.edit_firstname(new_firstname)

            elif user_choice == 2:
                print(f"Username: {username} has current surname '{username.surname}'")
                new_surname = self.set_surname(new_user=False)
                username.edit_surname(new_surname)

            elif user_choice == 3:
                print(f"Username: {username} has current email address '{username.email_address}'")
                new_email = self.set_email(new_user=False)
                username.edit_email_address(new_email)

            elif user_choice == 4:
                print(f"Username: {username} has current date of birth '{username.date_of_birth}'")
                new_dob = self.set_dob(new_user=False)
                username.edit_dob(new_dob)

            elif user_choice == 5:
                print("Returning to User Menu")
                return

    def users_sub_menu(self):
        """
        The main sub menu for handling our programmes users. Provides multiple options for the user such as:
        - Add new user: New users can be added to the system and saved to users_dict
        - Remove user: Users are searched up and can be removed from the users_dict
        - Edit user: An editor sub menu is displayed to the user where several user attributes can be updated
        - Total users: Displays to the user the total number of users in the system currently
        - User info: Displays in a neat format all information on record for a specific user

        - Utilises control_user_choice for clean and safe menu navigation

        """
        while True:
            print("\n--- Library System User Menu ---")
            print("Choose an option from the Sub Menu")
            print("1 - Add New User")
            print("2 - Remove a User")
            print("3 - Edit User Info")
            print("4 - Count Total Users")
            print("5 - Display User info")
            print("6 - Return to Main Menu")

            user_choice = control_user_choice("Enter here: ", range(1, 7))

            # Takes the user to the appropriate sub menu or quits the programme
            if user_choice == 1:
                self.add_new_user()

            elif user_choice == 2:
                self.remove_user_main()

            elif user_choice == 3:
                self.edit_user_menu()

            elif user_choice == 4:
                self.count_total_users()

            elif user_choice == 5:
                self.display_user_info()

            elif user_choice == 6:
                print("Returning to Main Menu..")
                break
