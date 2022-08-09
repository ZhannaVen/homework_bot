class NoDictionary(Exception):
    """От АРI-запроса ничего не пришло."""

    pass


class NoSuchStatus(Exception):
    """Статус работы не предусмотрен программой."""

    pass
