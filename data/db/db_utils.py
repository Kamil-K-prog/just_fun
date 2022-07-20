from typing import Callable

import datetime
from sqlalchemy.engine.default import DefaultExecutionContext


def get_current_yekt_datetime() -> datetime.datetime:
    ("""Возвращает объект datetime, содержащий текущее время """
     """в временной зоне Екатеринбурга (YEKT)""")
    return datetime.datetime.utcnow() + datetime.timedelta(hours=5)


def default_same_as(column_name: str) -> Callable:
    ("""Указывает SQLAlchemy, что значение по умолчанию для данной колонки """
     """должно быть взято из значения другой определённой колонки""")

    def default_function(context: DefaultExecutionContext) -> object:
        ("""Функция для передачи в параметр default """
         """при инициализации класса sqlalchemy.Column""")
        return context.current_parameters.get(column_name)
    return default_function
