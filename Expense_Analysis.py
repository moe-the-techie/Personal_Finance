import openpyxl
import time
from datetime import date

# Constants that signify the indexes of each attribute of an expense within the tuple
EXPENSE = 0
AMOUNT = 1
TYPE = 2
COMMENT = 3
DATE = 4


def wait():
    """
    Gives user time to read the report & prompts them to continue.
    """
    time.sleep(4)

    command = input("Enter \"c\" to continue: ").lower()

    if command != "c":
        print("Exiting program...")
        exit(0)


class DataBase:

    def __init__(self, file=None):

        try:

            if file is None or ".xlsx" not in file:
                raise ValueError

            # Initialize data dictionary and load data from file
            self.data = dict()
            self.file = file
            self.load_data(self.file)

        except ValueError:
            print("Usage: python main.py command file_name.xlsx\nPlease make sure the file entered is not empty and the"
                  " values start from the 2nd row with no gaps within the data.")
            exit(1)

        except FileNotFoundError:
            print("File not found")
            exit(2)

    def load_data(self, file):
        """
        Loads all data from a given file into the dataset.
        :param file: An Excel (.xlsx) file name stored in a string.
        """

        # Get active sheet from workbook
        wb = openpyxl.load_workbook(file, read_only=True)
        ws = wb.active

        # Ensure second row is not empty
        if ws.cell(row=2, column=2) is None:
            raise ValueError

        # Start from the 2nd row to ignore headers and map each date to a list of expenses each stored in a tuple.
        for i in range(2, ws.max_row + 1):
            if ws.cell(row=i, column=DATE + 1).value.date() not in self.data:
                self.data[ws.cell(row=i, column=DATE + 1).value.date()] = [(
                    ws.cell(row=i, column=EXPENSE + 1).value.lower(),
                    int(ws.cell(row=i, column=AMOUNT + 1).value),
                    ws.cell(row=i, column=TYPE + 1).value.lower().split(", "),
                    ws.cell(row=i, column=COMMENT + 1).value,
                    ws.cell(row=i, column=DATE + 1).value.date())]

            else:
                # Appending the expense to the day
                self.data[ws.cell(row=i, column=DATE + 1).value.date()]. \
                    append((ws.cell(row=i, column=EXPENSE + 1).value.lower(),
                            int(ws.cell(row=i, column=AMOUNT + 1).value),
                            ws.cell(row=i, column=TYPE + 1).value.lower().split(", "),
                            ws.cell(row=i, column=COMMENT + 1).value,
                            ws.cell(row=i, column=DATE + 1).value.date()))

        print("Data loaded successfully!\n")

    def maximum_expenses(self):
        """
        Finds the highest expense\s in the dataset.
        :return: A list of maximum expenses.
        """

        max_expense = (0, 0, 0, 0, 0)
        max_expense_list = list()

        # Assign the highest amount expense to max_expense
        for day in self.data:
            for expense in self.data[day]:
                max_expense = max_expense if max_expense[AMOUNT] > expense[AMOUNT] else expense

        # Add expenses that are equal to max_expense in amount to max_expense_list
        for day in self.data:
            for expense in self.data[day]:
                if expense[AMOUNT] == max_expense[AMOUNT]:
                    max_expense_list.append(expense)

        return max_expense_list

    def commented_expenses(self):
        """
        Gathers all the commented expenses in the dataset.
        :return: A list of all the commented expenses.
        """

        commented_expenses = list()

        for day in self.data:
            for expense in self.data[day]:
                if expense[COMMENT] is not None:
                    commented_expenses.append(expense)

        return commented_expenses

    def total_spending(self):
        """
        Calculates the total spending of the dataset.
        :return: A float representing the total spending.
        """

        total = 0

        for day in self.data:
            for expense in self.data[day]:
                total += expense[AMOUNT]

        return total

    def expense_average(self):
        """
        Calculates average spending per expense.
        :return: A float representing the average amount of all expenses.
        """

        total = 0
        count = 0

        for day in self.data:
            for expense in self.data[day]:
                total += expense[AMOUNT]
                count += 1

        return round(total / count, 2)

    def daily_average(self):
        """
        Calculates the average spending per day.
        :return: A float representing the average amount spent daily.
        """

        total = 0
        count = 0

        for day in self.data:
            count += 1
            for expense in self.data[day]:
                total += expense[AMOUNT]

        return round(total / count, 2)

    def type_averages(self):
        """
        Maps the average spending of each expense type to the type itself.
        :return: A dictionary mapping each expense type to it's average spending.
        """

        out = dict()

        type_count = self.expense_type_score()
        type_total = self.total_per_type()

        for expense_type in type_count:
            out[expense_type] = round(type_total[expense_type] / type_count[expense_type], 2)

        return out

    def expense_type_score(self):
        """
        Counts how often each expense type has showed up in the database.
        :return: Dictionary mapping each expense type to its score.
        """

        count = dict()

        for day in self.data:
            for expense in self.data[day]:
                for expense_type in expense[TYPE]:

                    if expense_type not in count:
                        count[expense_type] = 1
                    else:
                        count[expense_type] += 1

        return count

    def total_per_type(self):
        """
        Sums the spending of each expense type and maps each type to it's spending.
        :return: Dictionary mapping each expense type to its total spending.
        """

        out = dict()

        for day in self.data:
            for expense in self.data[day]:

                for expense_type in expense[TYPE]:

                    if expense_type not in out:
                        out[expense_type] = expense[AMOUNT]
                    else:
                        out[expense_type] += expense[AMOUNT]

        return out

    def most_frequent_expenses(self):
        """
        Gathers the top 5 most frequent expenses.
        :return: a dictionary mapping each of the top 5 expenses (string) to the number of times each showed up (int).
        """

        # Initial variables needed for the counting and ordering process
        count = dict()
        get_val = lambda x: count[x]

        # Count how often each expense has showed up
        for day in self.data:
            for expense in self.data[day]:
                if expense[EXPENSE] in count:
                    count[expense[EXPENSE]] += 1

                else:
                    count[expense[EXPENSE]] = 1

        # Sort the dictionary to find the top 5 expenses in frequency
        keys = list(count.keys())
        values = list(count.values())

        keys.sort(key=get_val, reverse=True)
        values.sort(reverse=True)

        out = dict()

        for i in range(5):
            out[keys[i]] = values[i]

        return out

    def trim_database(self, start, end):
        """
        Trims down the database to days that fall between a start and end date provided.
        :param start: String: representing the starting date of the range to trim down to.
        :param end: String: representing the ending date of the range to trim down to.
        :return: A dictionary with the same structure as self.data.
        """

        try:
            # Convert start and end into date objects
            day, month, year = start.split("-")
            day = int(day)
            month = int(month)
            year = int(year)
            start = date(year, month, day)

            day, month, year = end.split("-")
            day = int(day)
            month = int(month)
            year = int(year)
            end = date(year, month, day)

            if start not in self.data or end not in self.data or end <= start:
                raise ValueError

        except ValueError:
            print("Invalid Date entered")
            exit(1)

        # Trim down the database
        trimmed_db = dict()

        for day in self.data:
            if start <= day <= end:
                trimmed_db[day] = self.data[day]

        self.data = trimmed_db

    def day_report(self, day=None):
        """
        Creates a report on a single day for convenient and quick information retrival.
        :param day: A date object representing the day to report on.
        :return: A formatted string reporting on the expenses of the given day.
        """

        if day not in self.data:
            print("Date doesn't exist in Database.")
            exit(1)

        elif day is None:
            print("Please provide date.")
            exit(1)

        # The output string and initial variables
        out = "\nDAILY REPORT {day}:\nExpenses:\n".format(day=day)
        count = 0
        total = 0

        # Extract data and stats from database and format them into the output string
        for expense in self.data[day]:
            count += 1
            total += expense[AMOUNT]
            out += "{count}. {expense}, type: {type}, cost {amount}EGP. {comment}\n". \
                format(count=count,
                       expense=expense[EXPENSE].lower(),
                       type=expense[TYPE],
                       amount=expense[AMOUNT],
                       comment="" if expense[COMMENT] is None else expense[COMMENT])

        out += "\nStats:\ntotal spending = {total}EGP\naverage expense amount = {average}EGP\nno. expenses = {count}" \
               "".format(total=total,
                         average=round(total / count, 2),
                         count=count
                         )

        return out
