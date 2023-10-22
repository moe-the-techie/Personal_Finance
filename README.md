# Personal_Finance
A personal financing program that uses openpyxl (a Python module) to report on data provided in an Excel file particularly extracted from a notion database created to track daily expenses.

### Introduction:
While this project has an about-me dialogue that you can check out yourself by using it. I'd love to run you through the purpose and idea behind this project.
1. This application is meant to be a very basic command-line program that helps you calculate statistical attributes of your spending over a certain period of time.
2. The expense dataset used is an Excel file exported from a Notion database that I'll run you through in just a few lines.
3. This is my first solo project, and I'm open to learning how to optimize and take this project to the next level, as well as some praise for maybe not doing a horrible job? ;)
4. The program is created using Python, specifically using a library called [openpyxl](https://openpyxl.readthedocs.io), which helps extract and modify data in Excel workbooks.

### Prerequisites:
1. In order to track your daily expenses, you'll be using [Notion](notion.so), which is a note-taking & task management app available on all major operating systems. Notion helped me organize too many aspects of my life, one of which is tracking my expenses. I have created my own modular template which you can find in [this link](https://gelatinous-quince-abe.notion.site/Expenses-Tracking-d2b76ee7b4294dfeb0d8d635cd66403e?pvs=25). Now there are two things to keep in mind here with this Notion database, one is that you can add or remove any amount of expense types you want, but the properties of each expense should remain the same for the program to function properly, where you can change the names of the properties to whatever you want (for example you can change expense type to expense location where you enter where you spent your money). Still, it is preferred to use the database as is and only modify what expense types are supported.
2. Next you'll get the database template I've created to track my expenses (which also was the reason why I wanted to make this program), to get the database, you'll need to visit [this link](https://gelatinous-quince-abe.notion.site/Expenses-Tracking-d2b76ee7b4294dfeb0d8d635cd66403e?pvs=25) and click on duplicate to get the template into your notion account.
3. After inputting your daily expenses into the database, you'd be able to export your data as an Excel file by simply clicking the three dots in the top right corner of the database's page and scroll down -> export -> make sure to have Markdown & CSV selected, then hit export. Then open the CSV file using Excel, and save it as an Excel (.xlsx) file.
4. Now to run this program on your machine, you'll need Python installed to then enter the following command into your Python console (or any other terminal).

```
pip install openpyxl
```
### How to Run:
Having downloaded main.py, Expense_Analysis.py, and your Excel data file and stored them all in the same folder, you can go into the terminal and run the following:

```
python main.py command (your_file).xlsx
```
### Command guide:
- h --> prints initial user manual
- r --> launches reporting system
- a --> prints about me
- e --> exits the program

### Closing thoughts:
Thanks for taking the time to give this project a look! Feel free to contact me via Discord @moethetechie for any feedback, recommendation, offer, or if you just wanna chat for a bit. You can find [me on LinkedIn](https://www.linkedin.com/in/momen-ahmed-51b7301b8/) as well for my professional folks out there. It also goes without saying that I'd be delighted to review any pull requests or potential improvements to the project, have a wonderful day :D.
