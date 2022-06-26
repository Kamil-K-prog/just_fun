from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase


class Video(SqlAlchemyBase):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # кто прикрепил
    link = Column(Text, unique=True, nullable=True)  # или ссылка

    user = orm.relation('User')
