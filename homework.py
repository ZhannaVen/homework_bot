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
        encoding='utf-8',
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
    'approved': 'The work has been checked: the reviewer likes everything.',
    'reviewing': 'The work is being checked by the reviewer.',
    'rejected': 'The work has been checked: the reviewer has comments.'
}

TOKENS = (
    ('PRACTICUM_TOKEN', PRACTICUM_TOKEN),
    ('TELEGRAM_TOKEN', TELEGRAM_TOKEN),
    ('TELEGRAM_CHAT_ID', TELEGRAM_CHAT_ID),
)


def send_message(bot, message):
    """The function sends messages to the user."""
    try:
        logger.info(f'The message was sent: {message}')
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except telegram.error.TelegramError as error:
        logger.error(f'Error: {error}')
    else:
        logger.info('The message has been successfuly sent')


def get_api_answer(current_timestamp):
    """The function sends a request to a single endpoint of API service."""
    params_for_response = {
        'url': ENDPOINT,
        'headers': HEADERS,
        'params': {'from_date': current_timestamp},
    }
    try:
        logger.info(
            'API request with the following parameters:'
            '{url}, {headers}, {params}.'.format(**params_for_response)
        )
        response = requests.get(**params_for_response)
        if response.status_code != HTTPStatus.OK:
            raise InvalidResponseCode(
                f'Server response code: {response.status_code},'
                f'reason: {response.reason},'
                f'text: {response.json}'
            )
        return response.json()
    except Exception as error:
        raise ConnectionError(
            f'Error: {error}.'
            'API request has failed with the following parameters:'
            '{url}, {headers}, {params}.'.format(**params_for_response)
        )


def check_response(response):
    """The function checks API response for correctness."""
    logger.info('Start checking the API response for correctness')
    if not isinstance(response, dict):
        raise TypeError(logger.error('Answer is not a dictionary'))
    if 'homeworks' not in response:
        raise EmptyAPIReply('Empty response from API')
    homeworks = response.get('homeworks')
    if not isinstance(homeworks, list):
        raise KeyError('Answer is not a list')
    logger.info('All homework data has been received')
    return homeworks


def parse_status(homework):
    """The function extracts the status of the homework."""
    keys = (
        'homework_name',
        'status',
    )
    for key in keys:
        if key not in homework:
            raise KeyError(
                f'Homework {homework} does not contain such a key {key}'
            )
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_status not in HOMEWORK_VERDICTS:
        raise ValueError(
            f'Unexpected work status has been received: "{homework_status}".'
        )
    logger.info(f'Work status has been received {homework_name}')
    return (
        'The status of the work has changed "{homework_name}".'
        '{verdict}'.format(
            homework_name=homework_name,
            verdict=HOMEWORK_VERDICTS[homework_status]
        )
    )


def check_tokens():
    """The function checks the availability of environment variables."""
    TOKENS = (
        ('PRACTICUM_TOKEN', PRACTICUM_TOKEN),
        ('TELEGRAM_TOKEN', TELEGRAM_TOKEN),
        ('TELEGRAM_CHAT_ID', TELEGRAM_CHAT_ID),
    )
    token_checked = True
    for token, value in TOKENS:
        if not value:
            logger.critical(
                'Environment variable is missing : {}'.format(token)
            )
            token_checked = False
    return token_checked


def main():
    """The main logic of the bot."""
    if not check_tokens():
        raise InvalidTokens('An error has occured in environment variable(s)')
    logger.info('Token verification has completed successfully.')
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = 0
    current_report = {}
    previous_report = {}
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            if homeworks:
                homework = homeworks[0]
                message = parse_status(homework)
                current_report['message'] = message
            else:
                message = 'There is no homework'
                current_report['message'] = message
            if current_report != previous_report:
                send_message(bot, message)
                previous_report = current_report.copy()
                current_timestamp = response.get(
                    'current_date',
                    current_timestamp
                )
            else:
                logger.info('There are no new homework statuses')
        except NotForSending as error:
            message = 'Failure. Error: {}'
            logger.error(message.format(error))
        except Exception as error:
            message = 'Failure. Error: {}'
            logger.exception(message.format(error))
            current_report['message'] = message
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
