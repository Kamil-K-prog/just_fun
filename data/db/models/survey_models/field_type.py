from sqlalchemy import Column, Integer, Text
from sqlalchemy_serializer import SerializerMixin

from ...sqlalchemy_base_maker import SqlAlchemyBase


class FieldType(SqlAlchemyBase, SerializerMixin):
    """Тип поля универсальной формы для сбора информации"""
    __tablename__ = 'field_type'

    serialize_only = ('id', 'name')

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    # Наименование типа поля
    name = Column(Text, unique=True, nullable=False)
