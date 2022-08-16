from http import HTTPStatus
import logging
import os
import sys
import time

import requests
import telegram

from dotenv import load_dotenv

from exceptions import (
    EmptyAPIReply,
    InvalidResponseCode,
    InvalidTokens,
    NotForSending,
)


logger = logging.getLogger(__name__)
logger.addHandler(
    logging.StreamHandler(sys.stdout),

)
logger.addHandler(
    logging.FileHandler(
        os.path.join('main.log'),
        mode='a',
        encoding=None,
        delay=False
    )
)
load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

TOKENS = (
    ('PRACTICUM_TOKEN', PRACTICUM_TOKEN),
    ('TELEGRAM_TOKEN', TELEGRAM_TOKEN),
    ('TELEGRAM_CHAT_ID', TELEGRAM_CHAT_ID),
)


def send_message(bot, message):
    """Функция отправляет сообщения пользователю."""
    try:
        logger.info(f'Отправлено сообщение: {message}')
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except telegram.error.TelegramError as error:
        logger.error(f'Ошибка: {error}')
    else:
        logger.info('Сообщение было удачно отправлено')


def get_api_answer(current_timestamp):
    """Функция делает запрос к единственному эндпоинту API-сервиса."""
    params_for_response = {
        'url': ENDPOINT,
        'headers': HEADERS,
        'params': {'from_date': current_timestamp},
    }
    try:
        logger.info(
            'Запрос к API со следующими параметрами:'
            '{url}, {headers}, {params}.'.format(**params_for_response)
        )
        response = requests.get(**params_for_response)
        if response.status_code != HTTPStatus.OK:
            raise InvalidResponseCode(
                f'Код ответа сервера: {response.status_code},'
                f'причина: {response.reason},'
                f'текст: {response.json}'
            )
        return response.json()
    except ConnectionError as error:
        (
            f'Ошибка: {error}.'
            'Провалился запрос к API со следующими параметрами:'
            '{url}, {headers}, {params}.'.format(**params_for_response)
        )


def check_response(response):
    """Функция проверяет ответ API на корректность."""
    logger.info('Начало проверки ответа API на корректность')
    if not isinstance(response, dict):
        raise TypeError(logger.error('Ответ не является словарем'))
    if 'homeworks' not in response:
        raise EmptyAPIReply('Пустой ответ от API')
    homeworks = response.get('homeworks')
    if not isinstance(homeworks, list):
        raise KeyError('Ответ не является списком')
    logger.info('Получены данные всех домашних работ')
    return homeworks


def parse_status(homework):
    """Функция извлекает статус домашней работы."""
    keys = (
        'homework_name',
        'status',
    )
    for key in keys:
        if key not in homework:
            raise KeyError(
                f'Домашняя работа {homework} не содержит такой ключ {key}'
            )
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_status not in HOMEWORK_VERDICTS:
        raise ValueError(
            f'Получен неожиданный статус работы: "{homework_status}".'
        )
    logger.info(f'Получен статус домашней работы {homework_name}')
    return (
        'Изменился статус проверки работы "{homework_name}".'
        '{verdict}'.format(
            homework_name=homework_name,
            verdict=HOMEWORK_VERDICTS[homework_status]
        )
    )


def check_tokens():
    """Функция проверяет доступность переменных окружения."""
    TOKENS = (
        ('PRACTICUM_TOKEN', PRACTICUM_TOKEN),
        ('TELEGRAM_TOKEN', TELEGRAM_TOKEN),
        ('TELEGRAM_CHAT_ID', TELEGRAM_CHAT_ID),
    )
    for token, value in TOKENS:
        if value is None:
            logger.critical(
                'Отсутствует переменная окружения: {}'.format(token)
            )
            token_checked = True
            return not token_checked
    return True


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        raise InvalidTokens('Ошибка в переменной(ых) окружения')
    logger.info('Проверка токенов успешно завершена.')
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            if homeworks != 0:
                homework = homeworks[0]
                message = parse_status(homework)
                current_report = {}
                current_report[parse_status(homework)] = HOMEWORK_VERDICTS[
                    parse_status.homework.get('homework_status')]
            else:
                message = 'Нет ДЗ'
                current_report = {}
                current_report[''] = message
            previous_report = {}
            if current_report != previous_report:
                send_message(bot, message)
                previous_report = current_report.copy()
                time_from_response = response.get(time.time)
                current_timestamp = response.get('date', time_from_response)
            else:
                logger.info('Нет новых статусов ДЗ')
        except Exception:
            message = 'Какой-то сбой.'
            NotForSending(logger.exception(message))
            current_report = {}
            current_report[''] = message
            previous_report = {}
            if current_report != previous_report:
                send_message(bot, message)
                previous_report = current_report.copy()
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        filename='main.log',
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s,',
        filemode='a',
    )
    main()
