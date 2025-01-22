from Books import BookList
from Users import UserList
from Loans import Loans
from utils import control_user_choice


class LibraryProgramme:
    """
    Controls the flow and logic of our library system software. This class is the main entry point for the programme.
    It provides a user interface for navigating the Library system, allowing interaction with
    our Books, Users, and Loans classes, where users can manage these functionalities.
    """

    def __init__(self):
        self.book_list = BookList()
        self.user_list = UserList()
        self.loans = Loans(self.book_list, self.user_list)

    def library_menu(self):
        """
        Displays the main menu of the Library system and handles user navigation. Allows the user to access all
        functionalities of the system:
        Books: (add, search, remove, count total books, edit books)
        Users: (add, remove, edit users, count total users, display user info)
        Loans: (borrow, return, return all, find overdue books)
        """

        while True:
            print("\n--- Library System Main Menu ---")
            print("Choose an option from the Menu:")
            print("1 - Books")
            print("2 - Users")
            print("3 - Loans")
            print("4 - Quit")

            # Gets the users choice and ensures valid input by calling control_user_choice from utils.py
            user_choice = control_user_choice("Enter here: ", range(1, 5))

            # Takes the user to the appropriate sub menu or quits the programme
            if user_choice == 1:
                self.book_list.books_sub_menu()

            elif user_choice == 2:
                self.user_list.users_sub_menu()

            elif user_choice == 3:
                self.loans.loans_sub_menu()

            elif user_choice == 4:
                print("Exiting the Library System... Goodbye!")
                return


def main():
    """
    Main entry point of the programme
    """
    system = LibraryProgramme()
    system.library_menu()


if __name__ == "__main__":
    main()
