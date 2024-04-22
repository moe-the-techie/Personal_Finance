import openpyxl as xl
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import datetime as dt
import numpy as np
from PIL import Image

# Set display options to show all columns and rows
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Using Agg Renderer to generate plots
matplotlib.use('agg')

# Defaults for handling outliers and currency
handle_outliers = True
currency = "USD"


def load_data(file: str) -> pd.DataFrame:
    """
    Loads the data from the given Excel file into a pandas DataFrame.
    :param file: a string containing the name of a '.xlsx' file to load
    :return: pandas DataFrame that contains all the data loaded from the file
    """

    try:

        if not file.endswith('.xlsx'):
            raise FileNotFoundError()

        # Load workbook and assign the active sheet to a variable
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
                'amount': round(float(row[1].value), 2),
                'type': tuple(row[2].value.split(',')),
                'comment': row[3].value,
                'date': dt.datetime.strptime(row[4].value, '%B %d, %Y').date()
            }, ignore_index=True)

    except FileNotFoundError:
        print("File wasn't found, please make sure the file exists in the same directory"
              "as main.py, making sure that the file entered ends with '.xlsx'. And watch out for typos!")
        exit(1)

    except ValueError:
        print("Invalid data format, kindly make sure your .xlsx file is the one exported directly from Notion "
              "and that it has data stored within it.")
        exit(2)

    expenses.dropna(subset=['expense', 'amount', 'type', 'date'])

    print("Dataset loaded.", end="\n\n")

    if expenses.empty:
        print("Invalid data format, kindly make sure your .xlsx file is the one exported directly from Notion "
              "and that it has data stored within it.")
        exit(2)

    return expenses


def set_currency(in_currency: str) -> str:
    """
    Changes system currency to a given value and returns it to be changed in other modules.
    :param in_currency: str representing desired currency value
    :return: str representing capitalized notation of currency
    """
    global currency

    currency = in_currency.upper()

    return currency


def avg_per_unit(expenses: pd.DataFrame, interval: int) -> float:
    """
    Calculates the average spending per a given interval of time (in days).
    :param expenses: pandas dataframe containing expenses data
    :param interval: integer representing number of days on which the average is calculated
    :return: float representing average spending per day, rounded to two digits past the decimal place
    """

    expenses = remove_outliers_percentile(expenses)

    grouped = expenses.groupby('date')

    n_intervals = len(grouped) / interval

    total = total_spending(expenses)

    return round(total / n_intervals, 2)


def expense_avg(expenses: pd.DataFrame) -> float:
    """
    Calculates the average spending per expense.
    :param expenses: pandas DataFrame containing expense data
    :return: float representing average spending per expense, rounded to two digits past the decimal place
    """
    # Handle outliers first
    expenses = remove_outliers_percentile(expenses)

    return round(expenses['amount'].sum() / len(expenses), 2)


def total_spending(expenses: pd.DataFrame) -> float:
    """
    Calculates the total spending over the time range of the given dataframe.
    :param expenses: pandas DataFrame containing expense data
    :return: float representing the total spending
    """
    return round(expenses['amount'].sum(), 2)


def commented_expenses(expenses: pd.DataFrame) -> pd.DataFrame | str:
    """
    Getter function to get all expenses with comments.
    :param expenses: pandas DataFrame containing expense data
    :return: pandas DataFrame containing all commented expenses
    """
    commented = expenses.dropna(subset=['comment']).reset_index()

    if commented.empty:

        return "No commented expenses found."

    commented.drop(columns=['index'], inplace=True)

    return commented


def expense_type_averages(expenses: pd.DataFrame) -> None:
    """
    Plotting function that generates a bar chart of the average spending of each expense type in the given dataframe.
    :param expenses: pandas DataFrame containing expense data
    """

    # Average spending per expense type
    per_type_average = expenses.groupby('type')['amount'].mean()

    plot_type_data(per_type_average)


def expense_type_totals(expenses: pd.DataFrame) -> None:
    """
    Plotting function that generates a bar chart of the total spending of each expense type in the given dataframe.
    :param expenses: pandas DataFrame containing expense data
    """
    per_type_total = expenses.groupby('type')['amount'].sum()

    plot_type_data(per_type_total, total=True)


def plot_type_data(grouped_data: pd.Series, total: bool = False) -> None:
    """
    Helper function that generates bar charts using the data within the passed series given that it's grouped by type
    :param total: indicator used to signify whether the plot is for total spending or average spending
    :param grouped_data: pandas Series containing expense data grouped by type with sum or mean operation done on amount
    """

    # List of strings containing all expense types & type combinations in the dataframe
    expense_types = [', '.join(expense) if len(expense) > 1 else str(expense).strip("(,')") for expense in
                     grouped_data.index]

    # Adjust plot image size
    plt.figure(figsize=(12, 8))

    bars = grouped_data.plot(x='type', y='amount', kind='bar')

    # Use the expense_types list as the ticks for x-axis
    plt.xticks(range(len(expense_types)), expense_types, rotation=90)

    # Touch-ups to plot depending on whether we're displaying total spending or average spending data
    if total:
        plt.title('Total Spending')
        plt.ylabel(f'Total Amount Spent ({currency})')

    else:
        plt.title('Average Spending')
        plt.ylabel(f'Average Amount Spent ({currency})')

    plt.xlabel('Expense Type')

    for bar in bars.patches:
        plt.annotate(str(round(bar.get_height())),
                     (bar.get_x() + bar.get_width() / 2,
                      bar.get_height()),
                     ha='center',
                     va='center',
                     xytext=(0, 5),
                     textcoords='offset points')

    plt.tight_layout()

    plt.savefig(r"C:\Users\hp\Documents\GitHub\Personal_Finance\expense-type-chart")

    print(f"Plot generated successfully. Opening 'expense-type-chart'...", end="\n\n")

    # Open the image file using PIL and display it
    img = Image.open(r"C:\Users\hp\Documents\GitHub\Personal_Finance\expense-type-chart.png")
    img.show()


def change_time_range(start: str, end: str, expenses: pd.DataFrame) -> pd.DataFrame:
    """
    Trims down the time range of an expenses dataframe down to the given start (inclusive) & end (exclusive) dates
    :param start: string formatted "YYYY-MM-DD" signifying the start date (included)
    :param end: string formatted "YYYY-MM-DD" signifying the end date (excluded)
    :param expenses: pandas DataFrame containing expense data to trim down
    :return: pandas DataFrame containing expenses data during the given timeframe only
    """

    # Convert start and end dates to datetime.date objects
    start = dt.datetime.strptime(start, "%Y-%m-%d").date()
    end = dt.datetime.strptime(end, "%Y-%m-%d").date()

    # Ensures end and start dates are assigned correctly
    if start > end:
        tmp = start
        start = end
        end = tmp

    return expenses[(start <= expenses['date']) & (expenses['date'] < end)]


def frequent_expenses(expenses: pd.DataFrame) -> pd.DataFrame:
    """
    Finds the top ten most frequent expenses and reports on their frequency, average cost, and total spending
    :param expenses: pandas DataFrame containing expense data to analyze
    :return: pandas DataFrame reporting on the top 5 most frequent expenses
    """

    grouped = expenses.groupby('expense')
    counts = grouped.size()
    totals = grouped['amount'].sum()
    averages = round(totals / counts, 2)

    report = pd.DataFrame({
        'Total Spent': totals,
        'Average Cost': averages,
        'Frequency': counts
    })

    report.sort_values(by=['Count'], ascending=False, inplace=True)

    if max(report.Count.values.tolist()) <= 5:
        print("Notice that the most frequent expense in yor dataset only repeated 5 or less times, for statistical"
              " significance, try to run Personal Finance 2.0 on a dataset that spans over a long period of time for "
              "more useful analysis.")

    return report.iloc[0:10, ]


def top_expenses(expenses: pd.DataFrame) -> pd.DataFrame:
    """
    Getter function that retrieves the ten highest expenses in amount of the given dataframe
    :param expenses: pandas DataFrame containing expense data
    :return:  pandas DataFrame containing top 10 expenses
    """

    selection = expenses.drop_duplicates(subset=['expense']).sort_values(by='amount', ascending=False)

    return selection.iloc[0:10, [0, 1, 4]].reset_index(drop=True)


def remove_outliers_percentile(expenses: pd.DataFrame) -> pd.DataFrame:
    """
    Removes all values residing above the 99th percentile of the given expenses dataset, typically used to remove
    entries that are extremely high in amount.
    :param expenses: pandas DataFrame containing expense data
    :return: pandas DataFrame with the extreme expenses removed
    """

    if handle_outliers:
        print("\nRemoving outliers...", end='\n\n')

    else:
        return expenses

    value_at_percentile = np.percentile(expenses['amount'], 99)

    return expenses[expenses['amount'] <= value_at_percentile]


def percent_of_income(expenses: pd.DataFrame, income: int) -> float:
    """
    Calculates total percentage of income spent.
    :param expenses: pandas DataFrame containing expense data
    :param income: int representing total income over the dataset's time range
    :return: float representing percentage of total income spent rounded to two decimals
    """

    return round((expenses['amount'].sum() / income) * 100, 2)
