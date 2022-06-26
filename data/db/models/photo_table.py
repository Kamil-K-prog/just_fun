from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase


class Photo(SqlAlchemyBase):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # кто прикрепил
    path = Column(Text, unique=True, nullable=False) # путь

    user = orm.relation('User')
