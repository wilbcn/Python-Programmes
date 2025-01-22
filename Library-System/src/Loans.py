from utils import control_user_choice
from utils import retry_func
import datetime
from datetime import datetime, timedelta


class Loans:
    """
    Handles all operations related to borrowing and returning Books in the Library system.
    - book_list (BookList) - An instance of the BookList class to access the books dictionary
    - user_list (UserList) - An instance of the Userlist class to access the users dictionary
    - books_on_load (dict) - A dictionary that stores information on books that have been rented

    Contains the following methods:
    - borrow_book: Users can rent a book as long as its available stock wise
    - return_book: Users can return a book as long as they are renting it
    - return_all_books: Users can return all books that they are currently renting
    - find_overdue_books: Displays any overdue books. Overdue books are books that have not been returned
      within two weeks.
    """
    def __init__(self, book_list, user_list):
        self.books_on_loan = {}
        self.book_list = book_list
        self.user_list = user_list

    def borrow_book(self):
        """
        Takes user input to specify a single book in stock and allows a user to rent it. Gets the specific
        user that will rent a book via lookup_username, and then the title for rental via lookup_book. These
        two method calls utilise the book_list and user_list instances we initialised.

        Ensures there are existing users before proceeding, and checks if the user is already renting the specified
        book. Updates the book stock accordingly.
        """

        # Gets the user that will borrow the Book
        current_user = self.user_list.lookup_username()
        if not current_user:
            print("Exiting process as there are no users.")
            return

        print(f"You are now renting for: {current_user.username}")
        print("All Books must be returned within two weeks or will be marked as overdue")

        # Gets the title of the Book for rental
        book_to_rent = self.book_list.lookup_book()
        if not book_to_rent:
            print("Returning to Loans Menu")
            return

        # Check user is not already renting the specified Book
        for book_title, loan_details in self.books_on_loan.items():
            if loan_details['username'] == current_user.username and book_title == book_to_rent.title:
                print(f"User '{current_user.username}' is already renting this book {book_to_rent.title}")
                print(f"Reminder, this book is due on {loan_details['due_date']}")
                return

        if book_to_rent.stock > 0:
            print(f"Book '{book_to_rent.title}' was found and is available to rent.")

            # Set the loan records for overdue logic and save Book rental
            rented_time = datetime.now()
            due_date = rented_time + timedelta(weeks=2)

            # Saves our book on rental using the Book title as the key
            self.books_on_loan[book_to_rent.title] = {
                "username": current_user.username,
                "rented_on": rented_time,
                "due_date": due_date
            }

            # Update and deduct the current Book stock
            book_to_rent.stock -= 1
            print(f"'{book_to_rent.title}' is now being rented by {current_user.username}")
            print(f"Day of rental {rented_time}")
            print(f"Due date {due_date}")
            return
        else:
            print(f"'{book_to_rent.title} is currently out of stock. Please choose another Book to rent.")

    def return_book(self):
        """
        Takes user input to specify a single book in stock and allows a user to return it. Gets the specific
        user that will rent a book via lookup_username, and then the title for rental via lookup_book. These
        two method calls utilise the book_list and user_list instances we initialised.

        Creates a new dictionary to store current loaned books for the specified user, and reveals them neatly
        to the user. The user can then specify which book they would like to return. This method is for individual
        returns. We have another method for multi-returns.
        """

        # Get the user for Book return
        current_user = self.user_list.lookup_username()
        if not current_user:
            print("Exiting process as there are no users.")
            return

        # Find the books that are currently on loan for the current user
        current_user_loaned_books = {}

        for book_title, loan_details in self.books_on_loan.items():
            if loan_details['username'] == current_user.username:
                # Saves currently loaned books to a dictionary with the book title as its key
                current_user_loaned_books[book_title] = loan_details

        if not current_user_loaned_books:
            print(f"{current_user.username} has no books currently on loan.")
            return

        # Display to the current user which books are currently on Loan
        print(f"{current_user.username} is currently renting the below books:")
        for index, (book_title, loan_details) in enumerate(current_user_loaned_books.items(), start=1):
            print(f"\n{index} - Book title: {book_title}")
            print(f"Rented on: {loan_details['rented_on']}")
            print(f"Due date: {loan_details['due_date']}")

        # Gets the title of the Book for rental
        book_to_rent = self.book_list.lookup_book()
        if not book_to_rent:
            print("Returning to Loans Menu")
            return

        # Return the loaned book
        if book_to_rent.title in current_user_loaned_books:
            del self.books_on_loan[book_to_rent.title]
            print(f"Book titled '{book_to_rent.title}' has been successfully returned.")

            # Update stock
            book_to_rent.stock += 1
            print("Returning to Loans Menu")
            return
        else:
            print(f"Book titled {book_to_rent.title} is not currently being rented by "
                  f"this user {current_user.username}")
            if not retry_func("Retry with a different Book Title?"):
                print("Returning to Loans Menu")
                return

    def return_all_books(self):
        """
        Counts all Books a user is currently borrowing and provides options to return them all in one go.
        Gets the current user that will be returning books. Creates a new dictionary to add current loaned books
        and display to the user, as well as how many books (length of the new dictionary) they are renting.
        Utilises retry_func, as a pre-check to make sure the user really wants to return multiple books.
        If multiple books are returned, the relevant book stocks are updated accordingly.
        """

        # Get the user for Multi-Book return
        current_user = self.user_list.lookup_username()
        if not current_user:
            print("Exiting process as there are 0 users.")
            return

        # Find the books that are currently on loan for the current user
        current_user_loaned_books = {}

        for book_title, loan_details in self.books_on_loan.items():
            if loan_details['username'] == current_user.username:
                # Saves currently loaned books to a dictionary with the book title as its key
                current_user_loaned_books[book_title] = loan_details

        if not current_user_loaned_books:
            print(f"{current_user.username} has no books currently on loan.")
            return

        # Count and inform the user how many books they are currently renting
        print(f"{current_user.username} is currently renting {len(current_user_loaned_books)} book(s)")

        # Display to the current user which books are currently on Loan
        for index, (book_title, loan_details) in enumerate(current_user_loaned_books.items(),start=1):
            print(f"\n{index} - Book title: {book_title}")
            print(f"Rented on: {loan_details['rented_on']}")
            print(f"Due date: {loan_details['due_date']}")

        # Confirm if the user would like to return all rented books
        if retry_func("Return all books"):
            for book_title in list(current_user_loaned_books.keys()):
                del self.books_on_loan[book_title]

                # Update stock accordingly
                book = self.book_list.books_dict[book_title]
                book.stock += 1

                print(f"Book titled '{book_title}' has been successfully returned.")
            print(f"All books rented by {current_user.username} were returned.")
        else:
            print("Returning to Loans Menu")
            return

    def find_overdue_books(self):
        """
        Displays to the user any overdue books that are currently being rented by Library Users. A book is overdue when
        it has not been returned within two weeks from the day it was rented.
        Ensures there are books in the library system and also books on loan before proceeding.
        Utilises the datetime module and accesses values in our books_on_loan dictionary in order to calculate
        overdue books.
        """
        if not self.book_list.books_dict:
            print("There are no books in the Library System.")
            print("Returning to Loans Menu")
            return

        if not self.books_on_loan:
            print("There are no active books on loan.")
            print("Returning to Loans Menu")
            return

        today_date = datetime.now()
        overdue = False

        for book_title, loan_details in self.books_on_loan.items():
            user = loan_details['username']
            due_date = loan_details['due_date']

            if due_date < today_date:
                if not overdue:
                    print("--- Displaying Overdue Books ---")
                    overdue = True

                print(f"\nUser {user} has overdue books:")
                print(f"Book titled '{book_title}'. Was due on {due_date}")
                print(f"Days overdue: {(today_date - due_date).days}")

        if not overdue:
            print("No users have overdue books")
            print("Returning to Loans Main Menu")
            return

    def loans_sub_menu(self):
        """
        Provides the user with a sub menu for interacting with our Books. Provides multiple options including:
        - Borrow a book: Allows a user to borrow a book as long as its available and also not currently renting
        - Return a book: Allows a user to return a book as long as its currently on loan by that user
        - Return all books: Allows a user to return all books that are currently on loan by that user in one go
        - Find overdue books: Displays to the user, without specifying a user beforehand, all books that are overdue
          and for which users.

        - Utilises control_user_choice from Utils.py to safely navigate the sub menu.
        """
        while True:
            print("\n--- Library System Loans Menu ---")
            print("Choose an option from the Sub Menu")
            print("1 - Borrow a Book")
            print("2 - Return a Book")
            print("3 - Return all Books")
            print("4 - Find overdue Books")
            print("5 - Return to Main Menu")

            # Gets the users choice and ensures valid input by calling control_user_choice from utils.py
            user_choice = control_user_choice("Enter here: ", range(1,6))

            # Takes the user to the appropriate sub menu or quits the programme
            if user_choice == 1:
                self.borrow_book()

            elif user_choice == 2:
                self.return_book()

            elif user_choice == 3:
                self.return_all_books()

            elif user_choice == 4:
                self.find_overdue_books()

            elif user_choice == 5:
                print("Returning to Main Menu..")
                return



