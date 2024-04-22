# Personal_Finance (Version 2.0)
A personal financing program that uses openpyxl and pandas (Python modules) to extract spending data and apply statistical analysis on it using a simple command-line navigation system.

### Introduction:
Allow me to run you through the purpose and idea behind this project.
1. This application is meant to be an easy-to-use command-line python script that helps you calculate statistical attributes of your expenses data which is recorded over a certain period of time.
2. This is the second version of my first solo project as a developer, and I'm open to learning how to optimize and take this project to the next level.
3. The first version of the project stored data in a python dictionary, currently it uses a pandas dataframe which has improved speed and memory use drastically.

### Requirements & How to use:
1. In order to record your daily expenses, you'll be using [Notion](notion.so), which is a free note-taking & task management app available on all major operating systems. I have created my own modular template which you can find at [this link](https://gelatinous-quince-abe.notion.site/Expenses-Tracking-d2b76ee7b4294dfeb0d8d635cd66403e?pvs=25). The purpose of this Notion database is to record daily expenses and then have that data exported to be analyzed by Personal Finance.
2. Having Notion installed, you'll get the database template I've created to record daily expenses, simply visit [this link](https://gelatinous-quince-abe.notion.site/Expenses-Tracking-d2b76ee7b4294dfeb0d8d635cd66403e?pvs=25) and click on duplicate to get the template into your notion workspace.
3. Having recorded your expenses into the database over a decent period of time, you'll need to export your data as an Excel file by simply clicking the three dots in the top right corner of the database's page scroll down and hit export, making sure you have Markdown & CSV selected you can click exort. Then open the CSV file using Excel (or Google Spreadsheets), and save it as an Excel (.xlsx) file. And then make sure the .xlsx file is located in the program's source folder you've downloaded from this repository!
4. To install all required Python modules used by Personal Finance 2.0 you'll need to use any command line application (Windows powershell, git Bash, etc..) to navigate to the program's source folder and run the following command:

```
pip install -r requirements.txt
```
### How to Run:
Now to run Personal Finance 2.0 on your machine, you'll open the program's source folder in any IDE (e.g. VS Code or any similar text editor), making sure the Excel expense data file is inside, then open the main.py file and hit run. Or for the adept users, you can use any command line application to navigate to the source code folder and run main.py manually using command below and start using Personal Finance right away!

```
python main.py
```

### Closing thoughts:
Thanks for taking the time to give this project a look! Feel free to contact me via Discord @moethetechie for any feedback, recommendation, offer, or if you just wanna chat for a bit. You can find [me on LinkedIn](https://www.linkedin.com/in/momen-ahmed-51b7301b8/) as well for my professional folks out there. It also goes without saying that I'd be delighted to review any pull requests or potential improvements to the project.
