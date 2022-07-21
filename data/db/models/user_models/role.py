from sqlalchemy import Column, Integer, Text
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from ...sqlalchemy_base_maker import SqlAlchemyBase
from ...db_utils import versatile_represent, versatile_convert_to_str


class Role(SqlAlchemyBase, SerializerMixin):
    """Роль пользователя в системе"""
    __tablename__ = 'role'

    serialize_only = ('id', 'name')

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    name = Column(Text, unique=True, nullable=False)

    # Связи one-to-many:
    users = orm.relationship('User', lazy='select')

    __repr__ = versatile_represent

    __str__ = versatile_convert_to_str
