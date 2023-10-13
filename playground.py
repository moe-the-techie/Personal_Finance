import datetime
import openpyxl

wb = openpyxl.load_workbook("sample_file.xlsx")
ws = wb.active

te = {ws.cell(row=2,column=5).value.date():0}

print(datetime.date(day=25, month=7, year=2023) in te)
