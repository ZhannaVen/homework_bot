### Homework_bot - bot-assistant
### Description
 Telegram-bot обращается к API сервиса Практикум.Домашка и узнает статус вашей домашней работы: взята ли ваша домашка в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку

 Telegram-bot accesses the Praktikum.Homework API and finds out the status of your homework: whether your homework was reviewed, whether it was checked, and if it was checked, then the reviewer accepted it or returned it for revision


### Что делает бот? What does bot do?
- раз в 10 минут опрашивать API сервиса Практикум.Домашка и проверяет статус отправленной на ревью домашней работы;
- при обновлении статуса анализирует ответ API и отправляет вам соответствующее уведомление в Telegram;
- логирует свою работу и сообщает вам о важных проблемах сообщением в Telegram.

- once every 10 minutes, poll the Practicum.Homework API service and check the status of the homework sent for review;
- when updating the status, it analyzes the API response and sends you a corresponding notification in Telegram;
- logs its work and informs you about important problems with a message in Telegram.


### Как запустить проект (в Unix) How to run a project (on Unix)
- Клонировать репозиторий и перейти в него в командной строке.
Clone the repository and change into it on the command line.

```bash
git clone git@github.com:ZhannaVen/homework_bot.git
```
- Установите и активируйте виртуальное окружение (потребуется python версии >= 3.7):
Install and activate the virtual environment (requires python version >= 3.7):

```bash
py -3.7 -m venv venv
```

```bash
source venv/bin/activate
```

- Установите зависимости из файла requirements.txt

Install dependencies from requirements.txt file

```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

- Запустите проект:
Run the project:

```bash
python manage.py runserver
```