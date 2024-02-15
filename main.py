import Expense_Analysis
import datetime
import sys

REPORT_COMMANDS = ("enter report command:\n1 --> general stats report\n2 --> one day report\n3 --> choose time"
                   " range\n4 --> total spending\n5 --> expense average\n6 --> average daily spending\n7 -->"
                   " commented expenses\n8 --> highest cost expense/s\n9 --> expense type report\n10 --> "
                   "5 most frequent expenses\n0 --> exit program\n\ncommand: ")

TUTORIAL = ("Usage (type into terminal): python main.py command file.xlsx\nCommand list:\nh --> prints out initial "
            "user manual\nr --> launches reporting system\na --> prints about me\ne --> exits the program")

# I think this file could really use improvements, but this would mean changing the entire UI system from console
# commands to something more intuitive & in line with my vision. Will check on that later down the road.


def main():
    # Ensure valid input
    if len(sys.argv) <= 2:
        print(TUTORIAL)
        exit(1)

    command = sys.argv[1].lower()
    file = sys.argv[2]

    # Print based on command
    if command == "h":
        print(TUTORIAL)

    elif command == "r":
        print("Report System: Starting...")
        database = DataBase(file)

        command = input(REPORT_COMMANDS)
        report(database, command)

    elif command == "a":
        print("About me:\nThis project has been developed and is sustained by Momen Ahmed, a CS student at Cairo \n"
              "University, Egypt. Feel free to contact me via Discord or Instagram @moethetechie\nI am open to"
              "discussing this project (or others to come), and would love to help any fellow student/dev in need"
              " with a project or with studying computer science.\nI'm also open to freelancing gigs, feel free"
              "to send business inquiries/requests to the following email: moe@picassos.xyz")

    elif command == "e":
        print("Exiting program...")
        # Here you might want to clear memory before exiting
        exit(0)

    else:
        print("Invalid command. Use the command \"python main.py h your_file.xlsx\" for instructions on valid "
              "commands.\nTerminating process...")
        exit(1)


def report(database=None, command=None):
    """
    Executes a given command to print reports on the database.
    :param command: a one letter command entered by the user
    :param database: a database object that has all the data stored within it
    """

    try:
        command = int(command)

    except ValueError:
        print("Invalid command. Use command h for instructions on valid commands.\nTerminating process...")
        exit(1)

    if command is None or command not in range(11):
        print("Invalid command.")
        exit(1)

    elif database is None:
        print("No database provided, terminating process...")
        exit(2)

    elif command == 0:
        print("Thanks for using Personal_Finance!\nExiting program...")
        exit(0)

    elif command == 1:

        max_expense_list = database.maximum_expenses()

        max_expenses = "HIGHEST AMOUNT EXPENSE\S:\n"

        for i in range(1, len(max_expense_list) + 1):
            expense = max_expense_list[i - 1]
            max_expenses += "{i}. {name} (category: {type}) costing {amount} on {date}.\n" \
                .format(i=i,
                        name=str(expense[EXPENSE]).lower(),
                        type=expense[TYPE],
                        amount=expense[AMOUNT],
                        date=expense[DATE])

        print("\nTOTAL REPORT:\ntotal spending = {total_spending}\naverage (per expense) = {expense_average}\naverage"
              "(per day) = {day_average}\n\n{max_expenses}".format(total_spending=database.total_spending(),
                                                                   expense_average=database.expense_average(),
                                                                   day_average=database.daily_average(),
                                                                   max_expenses=max_expenses))

        print("end of report.\n")

        wait()
        report(database, input(REPORT_COMMANDS))

    elif command == 2:

        requested_day = None

        try:
            day, month, year = str(input("Enter date (format DD-MM-YYYY): ")).split("-")
            day = int(day)
            month = int(month)
            year = int(year)

            requested_day = datetime.date(day=day, month=month, year=year)

        except ValueError:
            print("\nInvalid date provided, terminating process..\n")
            exit(1)

        print(database.day_report(requested_day))

        print("\nend of report.\n")

        wait()
        report(database, input(REPORT_COMMANDS))

    elif command == 3:

        start = input("Enter start date (format DD-MM-YYYY): ")
        end = input("Enter end date (format DD-MM-YYYY): ")

        database.trim_database(start, end)

        print("\ndatabase updated\n")

        wait()
        report(database, input(REPORT_COMMANDS))

    elif command == 4:

        print("\nTOTAL SPENDING = {total}EGP\n".format(total=database.total_spending()))

        wait()
        report(database, input(REPORT_COMMANDS))

    elif command == 5:

        print("\nAVERAGE SPENDING PER EXPENSE = {avg}EGP\n".format(avg=database.expense_average()))

        wait()
        report(database, input(REPORT_COMMANDS))

    elif command == 6:

        print("\nAVERAGE DAILY SPENDING = {avg}EGP\n".format(avg=database.daily_average()))

        wait()
        report(database, input(REPORT_COMMANDS))

    elif command == 7:

        commented_expense_list = database.commented_expenses()

        commented_expenses = "COMMENTED EXPENSE\S:\n"

        for i in range(len(commented_expense_list)):
            expense = commented_expense_list[i]
            commented_expenses += "{i}. {name} (category: {type}) costing {amount}, comment \"{comment}\".\n" \
                .format(i=i,
                        name=expense[EXPENSE].lower(),
                        type=expense[TYPE],
                        amount=expense[AMOUNT],
                        comment=expense[COMMENT])

        print(commented_expenses)

        wait()
        report(database, input(REPORT_COMMANDS))

    elif command == 8:

        print("\nHIGHEST COST EXPENSE/S:")
        c = 1

        for expense in database.maximum_expenses():
            print("{c}. {expense}, purchased on {date}, costing {cost}EGP.".format(
                c=c,
                expense=expense[EXPENSE],
                date=expense[DATE],
                cost=expense[AMOUNT]
            ))

            c += 1

        print("\nend of report.\n")

        wait()
        report(database, input(REPORT_COMMANDS))

    elif command == 9:

        print("EXPENSE TYPE REPORT:")

        type_total = database.total_per_type()
        type_score = database.expense_type_score()
        type_average = database.type_averages()

        for expense_type in type_total:
            print(
                "(type: {expense_type}) total spending: {total}EGP, no. expenses: {score}, average: {average}EGP".format(
                    expense_type=expense_type,
                    total=type_total[expense_type],
                    score=type_score[expense_type],
                    average=type_average[expense_type]
                ))

        print("\nend of report.\n")

        wait()
        report(database, input(REPORT_COMMANDS))

    elif command == 10:

        print("\nTOP 5 EXPENSES:\n")

        top_five = database.most_frequent_expenses()
        c = 1

        for expense in top_five:
            print("{c}. expense: {expense}, frequency: {count}.".format(
                c=c,
                expense=expense,
                count=top_five[expense]
            ))
            c += 1

        print()

        wait()
        report(database, input(REPORT_COMMANDS))


if __name__ == "__main__":
    main()
