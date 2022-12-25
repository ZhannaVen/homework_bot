### HomeworkBot - bot-assistant
### Description
 Telegram-bot accesses the Ya.Praktikum.Homework API and finds out the status of your homework. There are three statuses:
 - is being reviewed;
 - has been checked and accepted;
 - has been checked and needed improvement.
### What does Bot do?
- Bot sends a request to the Ya.Practicum.Homework API service and receives the status of the homework sent for review every 10 minutes;
- upon updating the status, Bot analyzes the API response and sends you a corresponding notification to your Telegram chat;
- Bot logs its work and informs you about important problems with a message to your Telegram chat.
### How to run a project (on Unix)
- Clone the repository
```bash
git clone git@github.com:ZhannaVen/homework_bot.git
```
- Install and activate the virtual environment (requires python version >= 3.7):
```bash
py -3.7 -m venv venv
source venv/bin/activate
```
- Install all dependencies from requirements.txt file
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
- Start the project:
```bash
python manage.py runserver
```
