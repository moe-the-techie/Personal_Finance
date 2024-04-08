import expense_analysis as exal
import time
import re


def main():

    print("Welcome to Personal Finance 2.0! To get started, enter command 'h' to see supported commands!.", end="\n\n")

    command = prompt(['h', 'e', 'a'])

    if command == 'h':

        print("\nCommand List:\n1. h: prints supported commands list\n2. e: launches expense analysis system\n3. a: "
              "prints about me")

        time.sleep(5)

        exit(0)

    elif command == 'a':
        # TODO: revamp about me
        print()

    else:

        file = str(input('Enter dataset file name (must be .xlsx): '))

        dataset = exal.load_data(file)

        reporter(dataset)


def reporter(dataset) -> None:
    """
    Handles all reporting and communication with expense analysis system
    :param dataset: pandas DataFrame containing expenses data loaded using load_data
    """

    currency = exal.set_currency("USD")

    main_menu = ("Choose one of the following navigation options:\n0 -> Modify dataset.\n1 -> Expense type stats.\n2 ->"
                 " General stats.\n3 -> Expense standouts.\n4 -> Miscellaneous stats.\nq: Quit Personal Finance 2.0.\n"
                 "\nYour choice: ")

    submenu_0 = ("Modify dataset:\n1 -> Set dataset currency (default: USD).\n2 -> Change time-range.\n3 -> Statistical"
                 " outliers.\nr -> Return to main menu.\n\nYour choice: ")

    submenu_1 = ("Expense type stats:\n1 -> Expense type average (bar chart).\n2 -> Expense type sum (bar chart).\nr ->"
                 " Return to main menu.\n\nYour choice: ")

    submenu_2 = ("General stats:\n1 -> Total spending.\n2 -> Average spending per-expense.\n3 -> Average spending per-"
                 "custom time unit.\nr -> Return to main menu.\n\nYour choice: ")

    submenu_3 = ("Expense standouts:\n1 -> Most frequent expenses.\n2 -> Most expensive expenses.\n3 ->"
                 "Commented expenses.\nr -> Return to main menu.\n\nYour choice: ")

    submenu_4 = "Miscellaneous stats:\n1 -> Percentage of income spent.\nr -> Return to main menu.\n\nYour choice: "

    print(main_menu)

    command = prompt(['0', '1', '2', '3', '4', 'q'])

    # TODO: check if the nested if conditions below can be simplified into a matrix design (DP)

    if command == '0':
        print(submenu_0)

        command = prompt(['1', '2', '3', 'r'])

        if command == '1':
            currency = exal.set_currency(input("Currency (e.g. USD, EUR, CAD): "))

        if command == '2':
            start = input("Start date (inclusive): ")
            end = input("End date (exclusive): ")

            date_format = re.compile(r'^\d{4}-\d{2}-\d{2}$')

            while start == end or start not in dataset['date'].values or end not in dataset['date'].values:
                if start == end:
                    print("Start and end dates cannot be the same, please try again", end="\n\n")

                if start not in dataset['date'].values or end not in dataset['date'].values:
                    print("Make sure dates entered are present within the provided dataset.", end="\n\n")

                while not date_format.match(start) or not date_format.match(end):
                    print("Invalid date format entered, please try again.")

                    start = input("Start date (inclusive): ")
                    end = input("End date (exclusive): ")

            tmp = dataset

            dataset = exal.change_time_range(start=start, end=end, expenses=dataset)

            if dataset.isempty:
                print("No data found in given time range, reverting changes...")

                dataset = tmp

        if command == '3':

            print("Outliers are extreme data points in your expense data that can skew or alter the statistical "
                  "properties of the dataset, to avoid that, expense analysis system removes the top 1% of the data "
                  "which means the most expensive things in the dataset (Which tend to be outliers) are removed, "
                  "which means that only the very extreme values will be removed and the rest of the data will be "
                  "untouched.\n\nKindly note that the operation of removing outliers only takes place when calculating"
                  "averages or dealing with expense-type related stats to ensure data integrity.", end="\n\n")

            print("Would you like to force stop outlier handling system? (y/n): ")

            answer = input().lower()

            if answer in ['y', 'yes']:
                exal.handle_outliers = False

                print("\nOutlier handling system: OFF")

            else:
                exal.handle_outliers = True

                print("\nOutlier handling system: ON")

        else:
            # TODO: return to main menu
            raise NotImplementedError

    elif command == '1':
        print(submenu_1)

        command = prompt(['1', '2', 'r'])

        if command == '1':

            exal.expense_type_average(dataset)

        elif command == '2':

            exal.expense_type_total(dataset)

        else:
            # TODO: return to main menu
            raise NotImplementedError

    elif command == '2':
        print(submenu_2)

        command = prompt(['1', '2', '3', 'r'])

        if command == '1':
            print("Total spending: " + str(exal.total_spending(dataset)) + currency)

        elif command == '2':
            print("Average spending per-expense: " + str(exal.expense_avg(dataset)) + currency)

        elif command == "3":
            # TODO: modify exal function to support custom time unit, prompt user for said time unit, print the output.
            raise NotImplementedError

        else:
            # TODO: return to main menu
            raise NotImplementedError

    elif command == '3':
        print(submenu_3)

        command = prompt(['1', '2', '3', 'r'])

        if command == '1':
            print("Top 10 most frequent expenses:")
            print(exal.frequent_expenses(dataset))

        elif command == '2':
            print("Top 10 most expensive expenses:")
            print(exal.top_expenses(dataset))

        elif command == '3':
            print("Commented expenses:")
            print(exal.commented_expenses(dataset))

        else:
            # TODO: return to main menu
            raise NotImplementedError
    else:
        print(submenu_4)

        command = prompt(['1', 'r'])

        if command == '1':
            income = input("Enter income over the time span of the database: ")

            while not income.isnumeric():
                income = input("Please make sure to enter income correctly (do not include decimal points or commas): ")

            income = int(income)

            print(exal.percent_of_income(dataset, income))

        else:
            # TODO: return to main menu
            raise NotImplementedError

    # TODO: interactivity & prompt handling, testing.


def prompt(options: list) -> str:
    """
    Prompts user for input and ensures it's within a list of options.
    :param options: list of options that the command must be within
    :return: str containing outputted command converted to lowercase if command is a char
    """

    command = ''

    while command not in options:
        command = input('\nInvalid command entered, please try again: ').lower()

    return command
