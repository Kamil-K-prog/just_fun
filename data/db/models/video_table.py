from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase


class Video(SqlAlchemyBase):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    pass_id = Column(Integer, ForeignKey('passports.id'))  # кто прикрепил
    link = Column(Text, unique=True, nullable=True)  # или ссылка

    passport = orm.relation('Passport')
