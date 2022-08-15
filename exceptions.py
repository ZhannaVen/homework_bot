class NotForSending(Exception):
    """Ответы не для пересылки."""
    pass


class EmptyAPIReply(NotForSending):
    """Пришел пустой ответ от API."""
    pass


class InvalidTokens(NotForSending):
    """Ошибка в переменных окружения."""
    pass


class InvalidResponseCode(Exception):
    """Неверный код ответа сервера."""
    pass
