import random
import datetime
from datetime import datetime
from datetime import date
import calendar
from utils import control_user_choice
from utils import retry_func
from utils import validate_text


class Books:
    """
    Represents a single book in the Library System. Contains the following attributes:

    Title: The title of the book.
    Author: The author of the book.
    Book_id: A random and unique identifier for the book. Can be expanded from current 0-300.
    Publisher: The publisher of the book.
    Stock: The number of available copies for rental.
    Release_date: The date the book was released.

    Leverages methods from utils.py to clean and validate user input, and safely navigate sub menus.

    Setter methods (edit) - These methods are used in two different ways.
    - When creating a new book object (edit=False)
    - When editing an existing book attribute (edit=True)
    """

    def __init__(self, title, author, book_id, publisher, stock, release_date):

        self.title = title
        self.author = author
        self.book_id = book_id
        self.publisher = publisher
        self.stock = stock
        self.release_date = release_date

    def __str__(self):
        """Returns Book titles in string format"""
        return self.title

    def set_title(self, edit):
        """Takes user input to set the Title of the Book"""
        if not edit:
            print("Please input the title of the Book.")
            title = input("Enter here: ")
            validate_title = validate_text(title, "Title")
            print("Title accepted.")
            return validate_title
        elif edit:
            print("Please enter the new title for this Book")
            new_title = input("Enter here: ")
            validate_new_title = validate_text(new_title, "New Title")
            print("New title accepted")
            return validate_new_title

    def set_author(self, edit):
        """Takes user input to set the Author of the Book."""
        if not edit:
            print("Please input the Author of the book.")
            author = input("Enter here: ")
            validate_author = validate_text(author, "Author")
            print("Author accepted.")
            return validate_author
        elif edit:
            print("Please enter the new author for this Book")
            new_author = input("Enter here: ")
            validate_new_author = validate_text(new_author, "New Author")
            print("New author accepted")
            return validate_new_author

    def set_publisher(self, edit):
        """Takes user input to set the Publisher of the Book."""
        if not edit:
            print("Please input the Publisher of the book.")
            publisher = input("Enter here: ")
            validate_publisher = validate_text(publisher, "Publisher")
            print("Publisher accepted.")
            return validate_publisher
        elif edit:
            print("Please enter the new publisher for this Book")
            new_publisher = input("Enter here: ")
            validate_new_publisher = validate_text(new_publisher, "New Publisher")
            print("New publisher accepted")
            return validate_new_publisher

    def set_stock(self, edit):
        """Takes user input to set stock of the Book."""
        if not edit:
            print("Please specify how many books are in stock.")

        elif edit:
            print("Please specify the updated amount of books in stock.")

        while True:
            try:
                book_stock = int(input("Enter here: "))

                if book_stock <= 0:
                    print("Please enter an amount greater than 0.")
                else:
                    print("Stock amount accepted.")
                    return book_stock
            except ValueError:
                print("Amount cannot be empty and must be a number. Please try again.")

    def set_year(self):
        """Takes user to set the year the book was published."""
        print("Please input the year the book was released. E.g. 2010")
        current_year = datetime.now().year
        while True:
            try:
                year = int(input("Enter here: "))

                if len(str(year)) == 4:
                    if year <= current_year:
                        print(f"Year accepted.")
                        return year

                    else:
                        print("Year must not be greater than the current year.")
                else:
                    print("Invalid input. Year must be 4 numbers such as 2002.")

            except ValueError:
                print("Year cannot be empty and must be numbers only.")

    def set_month(self):
        """Takes user input to set the month of release"""
        months = list(calendar.month_name)[1:]  # Ensures we start at 1 as there is an index 0

        while True:
            try:
                print("Enter the month of release. E.g. July")
                get_month = input("Enter here: ").lower().capitalize()

                if get_month in months:
                    get_month = months.index(get_month) + 1  # Converts the month
                    print("Month accepted.")
                    return get_month

                else:
                    print("Month not recognised. Please try again.")

            except ValueError:
                print("Please input a valid month in text format.")

    def set_day(self):
        """Takes user input the set the day of release"""
        while True:
            try:
                print("Enter the day of release. E.g. 16")
                get_day = int(input("Enter here: "))

                if get_day > 0 or get_day <= 31:
                    return get_day

                else:
                    print("Please choose a day between 1-31.")

            except ValueError:
                print("Please input a number.")

    def set_release_date(self, edit):
        """Takes user input to set the release date of the Book."""
        if not edit:
            print("Please set the release date information for this new book")

        elif edit:
            print("Please set the updated release date information for this book.")

        book_year = self.set_year()
        book_month = self.set_month()
        book_day = self.set_day()

        # Calculate the release date.
        try:
            release_date = date(book_year, book_month, book_day)
            print(f"Book release date was set: {release_date}")
            return release_date

        except ValueError as e:
            print(f"Invalid date: {e}. Please try setting the release date again.")

    def return_title(self):
        """Returns the title of the book"""
        return self.title

    def return_author(self):
        """Returns the author of the book"""
        return self.author

    def return_book_id(self):
        """Returns the book_id of the book"""
        return self.book_id

    def return_publisher(self):
        """Returns the publisher of the book"""
        return self.publisher

    def return_stock(self):
        """Returns the stock of the book"""
        return self.stock

    def return_release_date(self):
        """Returns the release date of the book"""
        return self.release_date


class BookList:
    """
    Stores and organises our collection of books in the library system.
    This class provides multiple functionalities, including:
    - Add, search, remove, count total books, edit books
    - Generate unique IDs for each book
    - Display information to the user on the book collection
    - Save books in a dictionary for easy lookup

    - books_dict (dict) stores our books objects, using the book title as its key.

    - Leverages retry_func from utils.py, which provides the user the choice to retry whatever
      process they were performing. i.e. title was not found, retry.
    """

    def __init__(self):
        self.books_dict = {}

    def save_book(self, title, new_book):
        """Saves a book to the book's dictionary using the books title as the key."""
        self.books_dict[title] = new_book

    def gen_book_id(self):
        """Generates a random book ID when we create new book objects."""

        # Get existing book IDs to ensure no duplicates
        get_existing_book_ids = set()
        for book in self.books_dict.values():
            get_existing_book_ids.add(book.book_id)

        # Generate the random ID
        while True:
            book_id = random.randint(0, 299)
            if book_id not in get_existing_book_ids:
                return book_id  # Returns the book id to be passed on add_new_book

    def add_new_book(self):
        """
        Calls our setter methods to gather information in order to create a new book object.
        If 'edit' is False, the setter method carries out logic for a new book instance.
        If 'edit' is True, the setter method allows the user to change an existing book attribute.
        """

        book_id = self.gen_book_id()
        print(f"New book was created with ID: {book_id}")

        # Calls our Books class with default values in which we will later set when we call the setter methods.
        new_book = Books(title=" ", author=" ", book_id=book_id, publisher=" ", stock=0, release_date=None)

        # Call the setter methods to set each book attribute.
        new_book.title = new_book.set_title(edit=False)
        new_book.author = new_book.set_author(edit=False)
        new_book.publisher = new_book.set_publisher(edit=False)
        new_book.stock = new_book.set_stock(edit=False)
        new_book.release_date = new_book.set_release_date(edit=False)

        # Call the save book method to add the book to our dictionary.
        print(f"A new book titled: '{new_book.title}' was successfully added to the collection.")
        self.save_book(new_book.title, new_book)

    def lookup_book(self):
        """
        Searches for a book by Title in the books dictionary and returns it as a book object. Leveraged in multiple
        methods where we search for a book by its title for executing further operations.
        """
        if not self.books_dict:
            print("There are no Books in the Library System.")
            return False

        while True:
            print("Please enter the title of the Book.")
            title_to_find = input("Enter here: ")
            validate_title = validate_text(title_to_find, "Title")

            if validate_title in self.books_dict:
                return self.books_dict[validate_title]  # Returns the book object with the book title as its key.

            elif validate_title not in self.books_dict:
                print(f"No book was found with title: {validate_title}. Try again?")
                if not retry_func("Retry search"):
                    return False

    def search_library(self):
        """
        Searches the library for a specified Book in stock and displays to the user each attribute the book has.
        Uses the lookup_book method to get the Books title.
        """

        # Gets the title of the book for the search
        book = self.lookup_book()

        if not book or not isinstance(book, Books):
            print("Returning to Books Menu")
            return

        print(f"'{book}' was found.")
        print("Displaying information about this Book.")
        print(f"Title {book.title}")
        print(f"Author {book.author}")
        print(f"Book ID: {book.book_id}")
        print(f"Publisher: {book.publisher}")
        print(f"Number in stock: {book.stock}")
        print(f"Release date: {book.release_date}")
        return

    def remove_book(self):
        """
        Removes the specified book from the Library Collection. Uses the lookup_book method to get
        the books title.
        """

        # Gets the title of the book for removal
        book = self.lookup_book()
        if not book or not isinstance(book, Books):
            print("Returning to Books Menu")
            return

        print(f"'{book}' was found.")
        print("Are you sure you want to remove this Book?")
        if retry_func("Remove Book"):  # Calls retry_func from utils.py to allow the user to try again.
            del self.books_dict[book.title]
            print(f"{book} was removed from the Library Collection.")
            print("Returning to Books Menu")
            return
        else:
            print("No Books have been removed. Returning to Books Menu.")
            return

    def review_collection(self):
        """
        Counts the number of books in our books dictionary and displays this information to the user.
        """

        if not self.books_dict:
            print("There are currently 0 Books in the Collection")
            return None

        if len(self.books_dict) == 1:
            print("There is 1 Book in the Collection.")
        else:
            print(f"There are {len(self.books_dict)} Books in the Collection.")

    def edit_book_sub_menu(self):
        """
        Provides a sub menu for editing book attributes such as changing a books title or author.
        Utilises the setter methods from Books class, inserting an argument 'edit' for code re-usability.
        Calls lookup_book, and provides edit options for a specific book title, providing a clean and easy
        to use editor menu.

        - Utilises control_user_choice to safely navigate the editor sub menu.
        """

        # Get the title of the Book for edit
        book_to_edit = self.lookup_book()

        if not book_to_edit or not isinstance(book_to_edit, Books):
            print("Returning to Books Menu")
            return

        print(f"Displaying editor menu for Book titled: {book_to_edit}")
        while True:
            print("\n--- Library System Book Editor Menu ---")
            print("Choose an option from the Sub Menu:")
            print("1 - Edit Book Title")
            print("2 - Edit Book Author")
            print("3 - Edit Book Release Date")
            print("4 - Edit Book Publisher")
            print("5 - Edit Book Stock")
            print("6 - Return to Main Menu")

            user_choice = control_user_choice("Enter here: ", range(1, 7))

            if user_choice == 1:
                print(f"The book for edit currently has the title: '{book_to_edit}'")
                new_title = book_to_edit.set_title(edit=True)
                book_to_edit.title = new_title
                print(f"Title was successfully updated to {new_title}")

            elif user_choice == 2:
                print(f"The book for edit currently has the author: {book_to_edit.author}")
                new_author = book_to_edit.set_author(edit=True)
                book_to_edit.author = new_author
                print(f"Author was successfully updated to {new_author}")

            elif user_choice == 3:
                print(f"The book for edit currently has release date set to {book_to_edit.release_date}")
                new_release_date = book_to_edit.set_release_date(edit=True)
                book_to_edit.release_date = new_release_date
                print(f"Release date has been successfully changed to {new_release_date}")

            elif user_choice == 4:
                print(f"The book for edit currently has the publisher: {book_to_edit.publisher}")
                new_publisher = book_to_edit.set_publisher(edit=True)
                book_to_edit.publisher = new_publisher
                print(f"Publisher was successfully updated to {new_publisher}")

            elif user_choice == 5:
                print(f"The book for edit currently has {book_to_edit.stock} book(s) in stock.")
                new_stock = book_to_edit.set_stock(edit=True)
                book_to_edit.stock = new_stock
                print(f"The stock amount has been changed to {new_stock}")

            elif user_choice == 6:
                print("Returning to Main Menu..")
                return

    def books_sub_menu(self):
        """
        Provides the user with a sub menu for interacting with our Books.
        Users can perform a variety of options:
        - Adding a new book object to the library
        - Searching for a specific book by its title
        - Removing a specific book by its title
        - Counting the total number of books in our books dictionary
        - Editing book attributes

        - control_user_choice is utilised to safely navigate the Book sub menu.
        """
        while True:
            print("\n--- Library System Book Menu ---")
            print("Choose an option from the Sub Menu")
            print("1 - Add Book to Library")
            print("2 - Search for a Book")
            print("3 - Remove Book from Library")
            print("4 - Count Total Books")
            print("5 - Edit Book")
            print("6 - Return to Main Menu")

            # Gets the users choice and ensures valid input by calling control_user_choice from utils.py
            user_choice = control_user_choice("Enter here: ", range(1, 7))

            # Takes the user to the appropriate sub menu or quits the programme
            if user_choice == 1:
                self.add_new_book()

            elif user_choice == 2:
                self.search_library()

            elif user_choice == 3:
                self.remove_book()

            elif user_choice == 4:
                self.review_collection()

            elif user_choice == 5:
                self.edit_book_sub_menu()

            elif user_choice == 6:
                print("Returning to Main Menu..")
                return
