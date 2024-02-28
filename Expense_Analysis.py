import openpyxl as xl
import pandas as pd
import matplotlib.pyplot as plt

# Set display options to show all columns and rows
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def load_data(file: str) -> pd.DataFrame:
    """
    Loads the data from the given Excel file into a pandas DataFrame.
    :param file: a string containing the name of a '.xlsx' file to load
    :return: pandas DataFrame that contains all the data loaded from the file
    """

    # IDEA: We can have a test case here where if the loaded data is none to check if the file is formatted properly

    try:

        file = str(file)

        if not file.endswith('.xlsx'):
            raise ValueError('Invalid file format, please enter a file name ending with ".xlsx".')

        wb = xl.load_workbook(file)
        ws = wb.active

        expenses = pd.DataFrame({
            'expense': [],
            'amount': [],
            'type': [],
            'comment': [],
            'date': []
        })

        for i, row in enumerate(ws.iter_rows()):
            # Skip header row
            if i == 0:
                continue

            # Appending data
            expenses = expenses._append({
                'expense': row[0].value,
                'amount': float(row[1].value),
                'type': tuple(row[2].value.split(',')),
                'comment': row[3].value,
                'date': row[4].value
            }, ignore_index=True)

    except FileNotFoundError:
        print("File wasn't found, please make the file exists in the same directory"
              "as main.py. And watch out for typos!")
        exit(1)

    except ValueError as e:
        print(e)
        exit(2)

    expenses.dropna(subset=['amount'])

    return expenses


def daily_average(expenses: pd.DataFrame) -> float:
    """
    Calculates the average spending per day.
    :param expenses: Pandas dataframe containing expenses data.
    :return: float representing average spending per day, rounded to two digits past the decimal place.
    """
    daily_sum = expenses.groupby('date')['amount'].sum()
    total = daily_sum.sum()

    return round(total / len(daily_sum), 2)


def expenses_average(expenses: pd.DataFrame) -> float:
    """
    Calculates the average spending per expense.
    :param expenses: pandas DataFrame containing expense data.
    :return: float representing average spending per expense, rounded to two digits past the decimal place.
    """
    return round(expenses['amount'].sum() / len(expenses), 2)


def total_spending(expenses: pd.DataFrame) -> float:
    """
    Calculates the total spending over the time range of the given dataframe.
    :param expenses: pandas DataFrame containing expense data.
    :return: float representing the total spending.
    """
    return expenses['amount'].sum()


def get_commented_expenses(expenses: pd.DataFrame) -> pd.DataFrame:
    """
    Getter function to get all expenses with comments
    :param expenses: pandas DataFrame containing expense data
    :return: pandas DataFrame containing all commented expenses
    """
    return expenses[expenses['comment'].notna()]


def top_ten_expenses(expenses: pd.DataFrame) -> pd.DataFrame:
    """
    Getter function that retrieves the ten highest expenses in amount of the given dataframe
    :param expenses: pandas DataFrame containing expense data
    :return:  pandas DataFrame containing top 10 expenses
    """

    expenses = expenses.drop_duplicates(subset=['expense']).sort_values(by='amount', ascending=False)

    return expenses.iloc[0:10, ]


def expense_type_average(expenses: pd.DataFrame) -> None:
    """
    Plotting function that generates a bar chart of the average spending of each expense type in the given dataframe
    :param expenses: pandas DataFrame containing expense data
    """

    # Average spending per expense type
    per_type_average = expenses.groupby('type')['amount'].mean()

    # List of strings containing all expense types & type combinations in the dataframe
    expense_types = [', '.join(expense) if len(expense) > 1 else str(expense).strip("(,')") for expense in
                     per_type_average.index]

    # Adjust plot image size
    plt.figure(figsize=(12, 8))

    per_type_average.plot(x='type', y='amount', kind='bar')

    # Use the expense_types list as the ticks for x-axis
    plt.xticks(range(len(expense_types)), expense_types, rotation=90)

    # Touch-ups to plot
    plt.title('Average Spending per type')
    plt.xlabel('Expense Type/s')
    plt.ylabel('Average Spending (EGP)')
    plt.tight_layout()

    plt.show()

    print("Plot generated successfully.")

# TODO: function that reports on total spending of each expense type & spending over time
