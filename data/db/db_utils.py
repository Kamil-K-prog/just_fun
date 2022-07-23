from typing import Callable, Iterable, Tuple, Union

import datetime
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.engine.default import DefaultExecutionContext


from .sqlalchemy_base_maker import SqlAlchemyBase


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


def _get_column_names(
        model_class_or_obj: Union[
            DeclarativeMeta, SqlAlchemyBase]) -> Tuple[str]:
    ("""Вспомогательная функция, возвращающая названия колонок таблицы БД, """
     """к которой относится данная ORM-модель""")
    return tuple(col.name for col in model_class_or_obj.__table__.columns)


def _get_column_names_with_types(
        model: DeclarativeMeta, column_py_types: Iterable[type]) -> Tuple[str]:
    ("""Возвращает названия атрибутов(полей) определённой ORM-модели, """
     """соответствующие определённым python-типам """)
    return tuple(
        col.name for col in model.__table__.columns
        if col.type.python_type in column_py_types)


def _get_column_names_of_foreign_keys(model: DeclarativeMeta) -> Tuple[str]:
    ("""Возвращает названия атрибутов(полей) определённой ORM-модели, """
     """которые являются внешними ключами """)
    return tuple(
        col.name for col in model.__table__.columns if col.foreign_keys)


def _join_model_obj_kwargs(
        model_obj: SqlAlchemyBase,
        column_names: Iterable[str],
        map_function: Callable = repr) -> str:  # применяется ко всем значениям
    ("""Вспомогательная функция, возвращающая строковое представление """
     """именованых аргументов инициализатора класса ORM-модели данного """
     """объекта c значениями из данного объекта ORM-модели. Например: """
     """id=5, name='vasya', surname='pupkin'""")
    return ', '.join(
        f'{col_name}={map_function(getattr(model_obj, col_name))}'
        for col_name in column_names)


def versatile_represent(model_obj: SqlAlchemyBase) -> str:
    ("""Универсальный корвертер в строковое представление, """
     """которое будет являться валидным для исполнения,  """
     """любого объекта любой ORM-модели в этом проекте. """
     """Можно заменить им специальный метод __repr__""")
    inside_brackets = _join_model_obj_kwargs(
        model_obj, _get_column_names(model_obj), map_function=repr)

    return f'{model_obj.__class__.__name__}({inside_brackets})'


def versatile_convert_to_str(model_obj: SqlAlchemyBase) -> str:
    ("""Универсальный корвертер в строку любого объекта любой ORM-модели """
     """в этом проекте. Можно заменить им специальный метод __str__""")
    if hasattr(model_obj, 'serialize_only'):
        col_names = model_obj.serialize_only
    else:
        col_names = _get_column_names(model_obj)

    kwargs_str = _join_model_obj_kwargs(model_obj, col_names, map_function=str)

    return f'<{model_obj.__class__.__name__} {kwargs_str}>'
