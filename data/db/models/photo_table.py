from enum import unique
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase


class Photo(SqlAlchemyBase):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    pass_id = Column(Integer, ForeignKey('passports.id'))  # кто прикрепил
    filename = Column(Text, unique=True, nullable=False)

    passport = orm.relation('Passport')
