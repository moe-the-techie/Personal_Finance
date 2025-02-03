import expense_analysis as exal
import re
from tabulate import tabulate

# Setting initial currency.
currency = exal.set_currency("USD")


def main():

    print("\nWelcome to Personal Finance 2.0! To get started, enter one of the following commands:\n"
          "e: launches expense analysis system\na: prints about developer.")

    print("Your choice: ", end="")

    command = prompt(['e', 'a'])

    if command == 'a':
        print("\nHello there! My name is Momen Ahmed (Moe), I'm a passionate software developer with one year of "
              "experience in Python software development using libraries such as openpyxl,\nnumpy, and pandas for data "
              "analysis. Personal Finance 2.0 is the second iteration of my first solo project.\nYou can find me at "
              "@moethetechie on github, discord, and stackoverflow.")

    else:

        file = str(input('Enter expense CSV file name (must end with .csv): '))

        dataset = exal.load_data(file)

        reporter(dataset)


def reporter(dataset) -> None:
    """
    Handles all reporting and communication with expense analysis system
    :param dataset: pandas DataFrame containing expenses data loaded using load_data
    """

    global currency

    main_menu = ("Choose one of the following navigation options:\n1 -> Expense type stats.\n2 -> "
                 "General stats.\n3 -> Expense standouts.\n4 -> Miscellaneous stats.\n0 -> Modify dataset."
                 "\nq: Quit Personal Finance 2.0.\n\nYour choice: ")

    submenu_0 = (f"Modify dataset:\n1 -> Set dataset currency (default: {currency}).\n2 -> Change time-range.\n3 -> "
                 f"Statistical outliers.\nr -> Return to main menu.\n\nYour choice: ")

    submenu_1 = ("Expense type stats:\n1 -> Expense type average (bar chart).\n2 -> Expense type sum (bar chart).\nr ->"
                 " Return to main menu.\n\nYour choice: ")

    submenu_2 = ("General stats:\n1 -> Total spending.\n2 -> Average spending per-expense.\n3 -> Average spending per-"
                 "custom time unit.\nr -> Return to main menu.\n\nYour choice: ")

    submenu_3 = ("Expense standouts:\n1 -> Most frequent expenses.\n2 -> Most expensive expenses.\n3 -> "
                 "Commented expenses.\nr -> Return to main menu.\n\nYour choice: ")

    submenu_4 = "Miscellaneous stats:\n1 -> Percentage of income spent.\nr -> Return to main menu.\n\nYour choice: "

    while True:

        print(main_menu, end='')

        command = prompt(['0', '1', '2', '3', '4', 'q'])

        if command == 'q':
            print("Thanks for using Personal Finance 2.0!")
            exit(0)

        elif command == '0':
            print(submenu_0, end='')

            command = prompt(['1', '2', '3', 'r'])

            if command == '1':

                currency = exal.set_currency(input("Currency (e.g. USD, EUR, CAD): "))

                print(f"Currency set to {currency}.", end="\n\n")

            if command == '2':
                start = input("Start date in the format 'YYYY-MM-DD' (inclusive): ")
                end = input("End date in the format 'YYYY-MM-DD' (exclusive): ")

                date_format = re.compile(r'^\d{4}-\d{2}-\d{2}$')

                # Ensure correct date format is entered.
                while start == end or not date_format.match(start) or not date_format.match(end):

                    if start == end:
                        print("Start and end dates cannot be the same, please try again", end="\n\n")

                    if not date_format.match(start) or not date_format.match(end):
                        print("Invalid date format entered, please try again.")

                    start = input("Start date in the format 'YYYY-MM-DD' (inclusive): ")
                    end = input("End date in the format 'YYYY-MM-DD' (exclusive): ")

                tmp = dataset

                dataset = exal.change_time_range(start=start, end=end, expenses=dataset)

                if dataset.empty:
                    print("No data found in given time range, reverting changes...", end="\n\n")

                    dataset = tmp

                else:
                    print("Dataset time range updated successfully.", end="\n\n")

            if command == '3':

                print("\nOutliers are extreme data points in your expense data that can skew or alter the statistical "
                      "properties of the dataset, to avoid that, expense analysis system removes the top 1% of the data"
                      "\nwhich means the most expensive things in the dataset (Which tend to be outliers) are removed, "
                      "meaning that only the very extreme values will be removed and the rest of the data will be "
                      "untouched.\n\nKindly note that the operation of removing outliers only takes place when "
                      "calculating averages or dealing with expense-type related stats to ensure data integrity.",
                      end="\n\n")

                print("Would you like to force stop outlier handling system? (y/n): ", end='')

                answer = input().lower()

                if answer in ['y', 'yes']:
                    exal.handle_outliers = False

                    print("\nOutlier handling system: OFF", end="\n\n")

                else:
                    exal.handle_outliers = True

                    print("\nOutlier handling system: ON", end="\n\n")

            else:
                continue

        elif command == '1':
            print(submenu_1, end='')

            command = prompt(['1', '2', 'r'])

            if command == '1':

                exal.expense_type_averages(dataset)

            elif command == '2':

                exal.expense_type_totals(dataset)

            else:
                continue

        elif command == '2':
            print(submenu_2, end='')

            command = prompt(['1', '2', '3', 'r'])

            if command == '1':
                print("Total spending: " + str(exal.total_spending(dataset)) + currency, end="\n\n")

            elif command == '2':
                print("Average spending per-expense: " + str(exal.expense_avg(dataset)) + currency, end="\n\n")

            elif command == "3":
                print("Enter time interval in days: ", end='')
                interval = int(prompt([str(item) for item in list(range(len(dataset.groupby('date'))+1))]))

                print(f"Average spending per every {interval} day/s: " +
                      str(exal.avg_per_unit(dataset, interval=interval)) + currency, end="\n\n")

            else:
                continue

        elif command == '3':
            print(submenu_3, end='')

            command = prompt(['1', '2', '3', 'r'])

            if command == '1':
                print("Top 10 most frequent expenses:")
                print(tabulate(exal.frequent_expenses(dataset), headers='keys', tablefmt='fancy_grid'), end="\n\n")

            elif command == '2':
                print("Top 10 most expensive expenses:")
                print(tabulate(exal.top_expenses(dataset), headers='keys', tablefmt='fancy_grid'), end="\n\n")

            elif command == '3':
                print("Commented expenses:")
                commented = exal.commented_expenses(dataset)

                if type(commented) is str:
                    print(commented)
                else:
                    print(tabulate(exal.commented_expenses(dataset), headers='keys', tablefmt='fancy_grid'), end="\n\n")

            else:
                continue
        else:
            print(submenu_4, end='')

            command = prompt(['1', 'r'])

            if command == '1':
                income = input("Enter income over the time span of the database: ")

                while not income.isnumeric():
                    income = input("Please make sure to enter income correctly (do not include decimal points or "
                                   "commas): ")

                income = int(income)

                print("Percentage of income spent: " + str(exal.percent_of_income(dataset, income)), end="%\n\n")

            else:
                continue


def prompt(options: list) -> str:
    """
    Prompts user for input and ensures it's within a list of options.
    :param options: list of options that the command must be within
    :return: str containing outputted value converted to lowercase if command is a char
    """

    value = input()

    while value not in options:
        value = input('\nInvalid value entered, please try again: ').lower()

    return value


if __name__ == '__main__':
    main()
