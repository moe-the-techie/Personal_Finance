import expense_analysis as exal
import time
import sys

# TODO: total_stats_report, make sure user is prompted for currency
# IDEAS: more statistics that we can follow: percent of income spent - trends over time


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

    # TODO: full commands list, UX design, interactivity & prompt handling.
