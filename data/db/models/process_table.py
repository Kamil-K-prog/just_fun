from sqlalchemy import Column, Integer, Text, ForeignKey, Date, Boolean
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase


class Process(SqlAlchemyBase):
    __tablename__ = 'processes'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    passport_id = Column(Integer, ForeignKey('passports.id'))
    type = Column(Text)
    date = Column(Date)

    answer = orm.relation('Answer', back_populates='process')
    passport = orm.relation('Passport')
