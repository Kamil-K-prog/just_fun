from sqlalchemy import Column, Integer, Text
from sqlalchemy_serializer import SerializerMixin

from ...sqlalchemy_base_maker import SqlAlchemyBase
from ...db_utils import versatile_represent, versatile_convert_to_str
from config import AppConfig


class FieldType(SqlAlchemyBase, SerializerMixin):
    """Тип поля универсальной формы для сбора информации"""
    __tablename__ = 'field_type'
    __table_args__ = AppConfig.DB_TABLE_ARGS

    serialize_only = ('id', 'name')

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    # Наименование типа поля
    name = Column(Text, unique=True, nullable=False)

    __repr__ = versatile_represent

    __str__ = versatile_convert_to_str
