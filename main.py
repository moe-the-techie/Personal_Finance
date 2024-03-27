import expense_analysis as exal
import time
import sys


def main():

    print("Welcome to Expense Analysis 2.0! To get started, enter command 'h' to see supported commands!.", end="\n\n")

    command = str(input("command: ")).lower()

    while command not in ['h', 'e', 'a', 'q']:

        print("\nInvalid command, please try again. Use command 'h' for list of supported commands.", end="\n\n")

        command = input("command: ").lower()

    if command == 'h':

        print("\nCommand List:\n1. h: prints supported commands list\n2. e: launches expense analysis system\n3. a: "
              "prints about me\n4. q: quits the program")

        time.sleep(5)

        exit(0)

    elif command == 'a':
        # TODO: revamp about me
        print()

    elif command == 'e':

        file = str(input('Enter dataset file name (must be .xlsx): '))

        dataset = exal.load_data(file)

        reporter(dataset)

    else:

        print('\nThanks for using Expense Analysis 2.0 :)')

        time.sleep(2)

        exit(0)


def reporter(dataset) -> None:
    """
    Handles all reporting and communication with expense analysis system
    :param dataset: pandas DataFrame containing expenses data loaded using load_data
    """

    main_menu = ("Choose one of the following navigation options:\n0 -> Modify dataset.\n1 -> Expense type stats.\n2 ->"
                 " General stats.\n3 -> Expense standouts.\n4 -> Miscellaneous stats.\n\nYour choice: ")

    submenu_0 = ("Modify dataset:\n1 -> Set dataset currency.\n2 -> Change time-range.\n3 -> Statistical outliers.\nr -"
                 "> Return to main menu.\n\nYour choice: ")

    submenu_1 = ("Expense type stats:\n1 -> Expense type average (bar chart).\n2 -> Expense type sum (bar chart).\nr ->"
                 " Return to main menu.\n\nYour choice: ")

    submenu_2 = ("General stats:\n1 -> Total spending.\n2 -> Average spending per-expense.\n3 -> Average spending per-"
                 "custom time unit.\nr -> Return to main menu.\n\nYour choice: ")

    submenu_3 = ("Expense standouts:\n1 -> Most frequent expenses.\n2 -> Most expensive expenses.\n3 ->"
                 "Commented expenses.\nr -> Return to main menu.\n\nYour choice: ")

    submenu_4 = "Miscellaneous stats:\n1 -> Percentage of income spent.\nr -> Return to main menu.\n\nYour choice: "

    command = input(main_menu)

    while not command.isnumeric() or command not in ['0', '1', '2', '3', '4']:
        command = input('\nInvalid command entered, please try again: ')

    # TODO: interactivity & prompt handling, ensure reporting works as intended.
