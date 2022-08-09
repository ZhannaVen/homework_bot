import logging
import os
import sys
import time

import requests
import telegram

from dotenv import load_dotenv

from exceptions import NoDictionary, NoSuchStatus


logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s, %(funcName)s,',
    filemode='a',
)
logger = logging.getLogger(__name__)
logger.addHandler(
    logging.StreamHandler(sys.stdout)
)

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    '''Функция отправляет сообщения пользователю.'''
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logger.info('Сообщение отправлено.')
    except telegram.error.TelegramError as error:
        logger.error(f'Ошибка: {error}')


def get_api_answer(current_timestamp):
    '''Функция делает запрос к единственному эндпоинту API-сервиса.'''
    params = {'from_date': current_timestamp}
    response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    if response.status_code != 200:
        raise requests.ConnectionError('Сервер недоступен')
    return response.json()


def check_response(response):
    '''Функция проверяет ответ API на корректность.'''
    if type(response) is not dict and len(response) == 0:
        raise NoDictionary(logger.error('Ничего нет'))
    logger.info('Получены данные последней работы')
    return response['homeworks'][0]


def parse_status(homework):
    '''Функция извлекает из информации о конкретной
    домашней работе статус этой работы.
    '''
    keys = (
        'homework_name',
        'status',
    )
    for key in keys:
        if key not in homework:
            raise KeyError(logger.error(f'Ошибка ключа {key}'))
    if homework['status'] not in HOMEWORK_STATUSES:
        raise NoSuchStatus(logger.error('Статус работы - не предусмотрен'))
    homework_name = homework['homework_name']
    homework_status = homework['status']
    verdict = HOMEWORK_STATUSES[homework_status]
    logger.info('Получен статус')
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    '''Функция проверяет доступность переменных окружения,
    которые необходимы для работы программы.
    '''
    tokens = (
        ('PRACTICUM_TOKEN', PRACTICUM_TOKEN),
        ('TELEGRAM_TOKEN', TELEGRAM_TOKEN),
        ('TELEGRAM_CHAT_ID', TELEGRAM_CHAT_ID),
    )
    FAILED_TOKEN = ('Отсутствует переменная окружения: {}')
    for token, value in tokens:
        if value is None:
            logger.error(FAILED_TOKEN.format(token))
            return False
    logger.info('Проверка токенов успешно завершена.')
    return True


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logger.critical('Проверьте переменные окружения.')
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homework = check_response(response)
            message = parse_status(homework)
            send_message(bot, message)
            time.sleep(RETRY_TIME)
        except Exception as error:
            message = f'Какой-то сбой. См. ошибку: {error}'
            send_message(bot, message)
            logger.critical(message)
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
