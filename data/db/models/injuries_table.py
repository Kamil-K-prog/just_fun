from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase


class Injuries(SqlAlchemyBase):
    __tablename__ = 'injuries'

    passport_id = Column(Integer, ForeignKey('passports.id'), primary_key=True, nullable=False, autoincrement=True, unique=True)
    deceased_workers = Column(Text, nullable=False)  # погибшие
    severely_injured_workers = Column(Text, nullable=False)  # тяжело травмированные
    group_accidents = Column(Text, nullable=False)  # групповые несчастные случаи
    workers_with_simple_injuries = Column(Text, nullable=False)  # легкие травмы
    workers_with_micro_injuries = Column(Text, nullable=False)  # микротравмы

    passport = orm.relation('Passport')
