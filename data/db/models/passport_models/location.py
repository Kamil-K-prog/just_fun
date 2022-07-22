from sqlalchemy import Column, Integer, Text
from sqlalchemy_serializer import SerializerMixin

from ...sqlalchemy_base_maker import SqlAlchemyBase
from ...db_utils import versatile_represent, versatile_convert_to_str


class Location(SqlAlchemyBase, SerializerMixin):
    ("""Обобщённый адрес """
     """(скорее не столь конкретное название некого местоположения), """
     """нужен для поиска по паспортам и для отображения на тепловой карте""")
    __tablename__ = 'location'

    serialize_only = ('id', 'name')

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    name = Column(Text, unique=True, nullable=False)  # Наименование

    __repr__ = versatile_represent

    __str__ = versatile_convert_to_str
