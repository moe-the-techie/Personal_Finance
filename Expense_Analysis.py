import openpyxl as xl
import pandas as pd

# Functions: I'll try to keep the existing functions, making adjustments to what I see fits.


def load_data(file: str):
    """
    Loads the data from the given Excel file into a pandas DataFrame.
    :param file: a string containing the name of a '.xlsx' file to load
    :return: Dataframe that contains all the data loaded from the file
    """

    try:

        if not file.endswith('.xlsx'):
            raise ValueError('Invalid file format, only xlsx files are supported')

        wb = xl.load_workbook(file)
        ws = wb.active

        expenses = pd.DataFrame({
            'expense': [],
            'amount': [],
            'types': [],
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
                'types': row[2].value.split(),
                'comment': row[3].value,
                'date': row[4].value
            }, ignore_index=True)

    except FileNotFoundError:
        print("File wasn't found, please watch out for typos!")
        exit(1)

    except ValueError as e:
        print(e)
        exit(2)

    expenses.dropna(subset=['amount'])

    return expenses


def daily_average(expenses: pd.DataFrame):
    """
    Calculates the average spending per day.
    :param expenses: Pandas dataframe containing expenses data.
    :return: Float representing average spending per day, rounded to two digits past the decimal place.
    """
    daily_sum = expenses.groupby('date')['amount'].sum()
    total = daily_sum.sum()

    return round(total / len(daily_sum), 2)
