from Expense_Analysis import DataBase
import Expense_Analysis
import sys

REPORT_COMMANDS = "enter report command:\n1 --> general stats report\n2 --> one day report\n3 --> choose time" \
                  " range\n4 --> total spending\n5 --> expense average\n6 --> average daily spending\n7 -->" \
                  " commented expenses\n8 --> highest cost expenses\n9 --> expense type report\n10 --> " \
                  "5 most frequent expenses\n0 --> exit program"


def main():
    """
    Here We will take the console's input and create objects to handle the command at hand
    """

    if len(sys.argv) <= 2:
        print("Usage: python main.py command file.xlsx\nCommand list:\nh --> prints out initial user manual\nr -->"
              " launches reporting system\na --> prints about me\ne --> exits the program")
        exit(1)

    command = sys.argv[1].lower()
    file = sys.argv[2]

    if command == "h":
        print("Command list:\nh --> prints initial user manual\nr --> launches reporting system\na --> prints"
              " about me\ne --> exits the program")

    elif command == "r":
        print("Report System: Starting...")
        db = DataBase(file)

        command = int(
            input(REPORT_COMMANDS))

        report(db, command)

    elif command == "a":
        print("About me:\nThis project has been developed and is sustained by Momen Ahmed, a CS student at Cairo \n"
              "University, Egypt. Feel free to contact me via Discord or Instagram @moethetechie\nI am open to"
              "discussing this project (or others to come), and would love to help any fellow student/dev in need"
              " with a project or with studying computer science.\nI'm also open to freelancing gigs, feel free"
              "to send business inquiries/requests to the following email: moe@picassos.xyz")

    elif command == "e":
        print("Exiting program...")
        exit(0)

    else:
        print("Invalid command. Use command h for instructions on valid commands.\nTerminating process...")
        exit(1)


def report(database=None, command=None):
    """
    Executes a given command to print reports on the database.
    :param command: a one letter command entered by the user
    :param database: a database object that has all the data stored within it
    """

    if command is None or command not in range(11):
        print("Invalid command.")
        exit(1)

    elif database is None:
        print("No database provided, terminating process...")
        exit(2)

    elif command == 0:
        print("Exiting program...")
        exit(0)

    elif command == 1:

        max_expense_list = database.maximum_expenses()

        max_expenses = "HIGHEST AMOUNT EXPENSE\S:\n"

        for i in range(len(max_expense_list)):
            expense = max_expense_list[i]
            max_expenses += "{i}. {name} (category: {type}) costing {amount} on {date}.\n" \
                .format(i=i,
                        name=expense[Expense_Analysis.EXPENSE].lower(),
                        type=expense[Expense_Analysis.TYPE],
                        amount=expense[Expense_Analysis.AMOUNT],
                        date=expense[Expense_Analysis.DATE])

        print("\nTOTAL REPORT:\ntotal spending = {total_spending}\naverage (per expense) = {expense_average}\naverage"
              "(per day) = {day_average}\n\n{max_expenses}".format(total_spending=database.total_spending(),
                                                                   expense_average=database.expense_average(),
                                                                   day_average=database.daily_average(),
                                                                   max_expenses=max_expenses))

        print("end of report.")

        report(int(input(REPORT_COMMANDS)))

    elif command == 2:

        day = str(input("Enter date (format DD-MM-YYYY): "))

        print(database.day_report(day))

        print("end of report.")

        report(int(input(REPORT_COMMANDS)))

    elif command == 3:
        start = input("Enter start date (format DD-MM-YYYY): ")
        end = input("Enter end date (format DD-MM-YYYY): ")

        database = database.get_trimmed_database(start, end)

        print("database updated")

        report(int(input(REPORT_COMMANDS)))

    elif command == 4:
        print("TOTAL SPENDING = {total}".format(total=database.total_spending()))

        report(int(input(REPORT_COMMANDS)))

    elif command == 5:
        print("AVERAGE SPENDING PER EXPENSE = {avg}".format(avg=database.expense_average()))

        report(int(input(REPORT_COMMANDS)))

    elif command == 6:
        print("AVERAGE DAILY SPENDING = {avg}".format(avg=database.daily_average()))

        report(int(input(REPORT_COMMANDS)))

    elif command == 7:

        commented_expense_list = database.commented_expenses()

        commented_expenses = "COMMENTED EXPENSE\S:\n"

        for i in range(len(commented_expense_list)):
            expense = commented_expense_list[i]
            commented_expenses += "{i}. {name} (category: {type}) costing {amount} on {date}.\n" \
                .format(i=i,
                        name=expense[Expense_Analysis.EXPENSE].lower(),
                        type=expense[Expense_Analysis.TYPE],
                        amount=expense[Expense_Analysis.AMOUNT],
                        date=expense[Expense_Analysis.DATE])

        print(commented_expenses)

        report(int(input(REPORT_COMMANDS)))


if __name__ == "__main__":
    main()
