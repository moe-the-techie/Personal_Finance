import openpyxl as xl
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np

# Set display options to show all columns and rows
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

handle_outliers = True


def load_data(file: str) -> pd.DataFrame:
    """
    Loads the data from the given Excel file into a pandas DataFrame.
    :param file: a string containing the name of a '.xlsx' file to load
    :return: pandas DataFrame that contains all the data loaded from the file
    """

    # IDEA: We can have a test case here where if the loaded data is none to check if the file is formatted properly

    try:

        if not file.endswith('.xlsx'):
            raise ValueError('Invalid file format, please enter a file name ending with ".xlsx".')

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
              "as main.py. And watch out for typos!")
        exit(1)

    except ValueError as e:
        print(e)
        exit(2)

    expenses.dropna(subset=['amount'])

    print("Dataset loaded.", end="\n\n")

    return expenses


def daily_avg(expenses: pd.DataFrame) -> float:
    """
    Calculates the average spending per day.
    :param expenses: Pandas dataframe containing expenses data.
    :return: float representing average spending per day, rounded to two digits past the decimal place.
    """
    daily_sum = expenses.groupby('date')['amount'].sum()

    total = daily_sum.sum()

    return round(total / len(daily_sum), 2)


def expense_avg(expenses: pd.DataFrame) -> float:
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


def commented_expenses(expenses: pd.DataFrame) -> pd.DataFrame | None:
    """
    Getter function to get all expenses with comments
    :param expenses: pandas DataFrame containing expense data
    :return: pandas DataFrame containing all commented expenses
    """
    commented = expenses.dropna(subset=['comment']).reset_index()

    if commented.empty:
        print('No commented expenses found.')

        return None

    return commented


def expense_type_average(expenses: pd.DataFrame) -> None:
    """
    Plotting function that generates a bar chart of the average spending of each expense type in the given dataframe
    :param expenses: pandas DataFrame containing expense data
    """

    # Average spending per expense type
    per_type_average = expenses.groupby('type')['amount'].mean()

    plot_type_data(per_type_average)


def expense_type_total(expenses: pd.DataFrame) -> None:
    """
    Plotting function that generates a bar chart of the total spending of each expense type in the given dataframe
    :param expenses: pandas DataFrame containing expense data
    """
    per_type_total = expenses.groupby('type')['amount'].sum()

    plot_type_data(per_type_total, total=True)

    print("Plot generated successfully.")


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

    grouped_data.plot(x='type', y='amount', kind='bar')

    # Use the expense_types list as the ticks for x-axis
    plt.xticks(range(len(expense_types)), expense_types, rotation=90)

    # Touch-ups to plot depending on whether we're displaying total spending or average spending data
    if total:
        plt.title('Total Spending Per-Type')
        plt.ylabel('Total Amount Spent (EGP)')

    else:
        plt.title('Average Spending Per-Type')
        plt.ylabel('Average Amount Spent (EGP)')

    plt.xlabel('Expense Type/s')
    plt.tight_layout()
    plt.show()

    print("Plot generated successfully.")


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

    # IDEA: If the most frequent expense only shows up say 10 times or a statistically insignificant number of times
    #  we can print "Insufficient data" and exit the function.

    grouped = expenses.groupby('expense')
    counts = grouped.size()
    totals = grouped['amount'].sum()
    averages = totals / counts

    report = pd.DataFrame({
        'Total Spent': totals,
        'Average Cost': averages,
        'Count': counts
    })

    report.sort_values(by=['Count'], ascending=False, inplace=True)

    return report.iloc[0:10, :]


def top_expenses(expenses: pd.DataFrame) -> pd.DataFrame:
    """
    Getter function that retrieves the ten highest expenses in amount of the given dataframe
    :param expenses: pandas DataFrame containing expense data
    :return:  pandas DataFrame containing top 10 expenses
    """

    selection = expenses.drop_duplicates(subset=['expense']).sort_values(by='amount', ascending=False)

    return selection.iloc[0:10, ]


def remove_outliers_percentile(expenses: pd.DataFrame) -> pd.DataFrame:
    """
    Removes all values residing above the 99th percentile of the given expenses dataset, typically used to remove
    entries that are extremely high in amount
    :param expenses: pandas DataFrame containing expense data
    :return: pandas DataFrame with the extreme expenses removed
    """

    value_at_percentile = np.percentile(expenses['amount'], 99)

    return expenses[expenses['amount'] <= value_at_percentile] if handle_outliers else expenses


def percent_of_income(expenses: pd.DataFrame, income: int) -> float:
    """
    Calculates total percentage of income spent.
    :param expenses: pandas DataFrame containing expense data
    :param income: int representing total income over the dataset's time range
    :return: float representing percentage of total income spent rounded to two decimals
    """

    return round((expenses['amount'].sum() / income) * 100, 2)
