import openpyxl as xl
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

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
                'date': dt.datetime.strptime(row[4].value, '%B %d, %Y').date()
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
    Trims down the time range of an expenses dataframe down to the given start & end dates
    :param start: string formatted "YYYY-MM-DD" signifying the starting date
    :param end: string formatted "YYYY-MM-DD" signifying the starting date
    :param expenses: pandas DataFrame containing expense data to trim down
    :return: pandas DataFrame containing expenses data during the given timeframe only
    """

    try:
        # Convert start and end dates to datetime.date objects
        start = dt.datetime.strptime(start, "%Y-%m-%d").date()
        end = dt.datetime.strptime(end, "%Y-%m-%d").date()

        if start > end or start not in expenses['date'].values or end not in expenses['date'].values or end == start:
            raise ValueError

    except ValueError:
        print("Invalid date/s entered. Please try again, making sure the start and end dates are within the provided "
              "dataset.")

        # TODO: try again by possibly re-prompting here or re-calling a certain function & ensure prompt explains
        #  that start date is inclusive and end date is exclusive

    return expenses[(start <= expenses['date']) & (expenses['date'] < end)]


if __name__ == '__main__':
    df = load_data('Expenses.xlsx')

    print(change_time_range('2023-10-1', '2024-1-1', df))

