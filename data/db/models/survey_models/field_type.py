from sqlalchemy import Column, Integer, Text

from ...sqlalchemy_base_maker import SqlAlchemyBase


class FieldType(SqlAlchemyBase):
    """Тип поля универсальной формы для сбора информации"""
    __tablename__ = 'field_type'

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    # Наименование типа поля
    name = Column(Text, unique=True, nullable=False)
