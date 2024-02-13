import openpyxl as xl
import pandas as pd

# Structure: I'll be reading in the file row by row, entering the data into a dictionary that'll be used for the
# creation of our desired dataframe.

# Functions: I'll try to keep the existing functions, making adjustments to what I see fits.


def load_data(file):
    """
    Loads the data from the given Excel file into a pandas DataFrame.
    :param file: .xlsx file to load
    """

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


if __name__ == '__main__':
    load_data('Expenses.xlsx')
