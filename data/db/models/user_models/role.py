from sqlalchemy import Column, Integer, Text
from sqlalchemy import orm

from ...sqlalchemy_base_maker import SqlAlchemyBase


class Role(SqlAlchemyBase):
    """Роль пользователя в системе"""
    __tablename__ = 'role'

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    name = Column(Text, unique=True, nullable=False)

    # Связи one-to-many:
    users = orm.relationship('User', lazy='select')
