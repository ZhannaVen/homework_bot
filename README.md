### HomeworkBot - is your bot-assistant
### Description
 Telegram-bot accesses the Ya.Praktikum.Homework API and finds out the status of your homework. There are three statuses:
 - reviewing (is being reviewed);
 - approved (has been checked and accepted);
 - rejected (has been checked and needed improvement).
### What does Bot do?
- Bot sends a request to the Ya.Practicum.Homework API service and receives the status of the homework sent for review every 10 minutes;
- upon updating the status, Bot analyzes the API response and sends you a corresponding notification to your Telegram chat;
- Bot logs its work and informs you about important problems with a message to your Telegram chat.
### Where requests are sent?
- Ya.Praktikum.Homework Endpoint - https://practicum.yandex.ru/api/user_api/homework_statuses/ (token-only access)
### .env file description template
PRACTICUM_TOKEN=<your secret token for access to Ya.Practicum, that only students have>
TELEGRAM_TOKEN=<secret token of your telegram bot>
TELEGRAM_CHAT_ID=<id of the chat where you want to forward a messadge of a homework status>
### Where Telegram_chat_id and Telegram_token can be found?
- Telegram_chat_id: find @userinfobot, send any message (or resend someone's else message) and Bot will reply you with chat_id;
- Telegram_token: find @BotFather, create your own Bot by following the instructions and then request secret token of your Bot.

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

