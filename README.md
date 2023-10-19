# Personal_Finance
A personal financing program that uses openpyxl (a Python module) to report on data provided in an Excel file particularly extracted from a notion database created to track daily expenses.

### Introduction:
While this project has an about me page that we'll explore later, I'll gladly run you through the purpose and details of this project briefly
1. This application is meant to be a very basic command-based program that helps you calculate statistical parameters about your expenses easily and quickly.
2. The expense dataset used is an Excel file, the steps to set up your expense tracking system and how to export data will be explained further in this readme.
3. This is my first solo project, and I'm open to learning how to optimize and take this project to the next level, as well as some praise for maybe not doing a horrible job? ;)
  4. The program is created using Python, specifically using a library called [openpyxl](https://openpyxl.readthedocs.io), which helps extract and modify data in Excel workbooks.

### Prerequisites:
1. In order to track your daily expenses, you'll be using [Notion](notion.so), which is a note-taking & task management app that helped me organize too many aspects of my life to mention, one of which is expense tracking. I have created my own modular template which you can find in [this link](). Now there are two things to keep in mind here with this Notion database, one is that you can add or remove any amount of expense types you want, but the properties of each expense should remain the same for the program to function properly, where you can change the names of the properties to whatever you want (for example you can change expense type to expense location where you enter where you spent your money) but it is preferred to use the database as is and only modify what expense types are supported.
2. Next you'll get the database template I've created to track my expenses (which also was the reason why I wanted to make this program), to get the database, you'll need to visit [this link](https://gelatinous-quince-abe.notion.site/Expenses-Tracking-d2b76ee7b4294dfeb0d8d635cd66403e?pvs=25) and click on duplicate to get the template into your notion account.
3. Now for the requirements of the program itself, to run this program on your machine, you'll need Python installed to then enter the following command into your Python console (or any other terminal).

```
pip install openpyxl
