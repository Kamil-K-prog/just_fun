from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy import orm

from ...sqlalchemy_base_maker import SqlAlchemyBase


class Injuries(SqlAlchemyBase):
    """Производственный травматизм в организации"""
    __tablename__ = 'injuries'

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    passport_id = Column(
        Integer, ForeignKey('passport.id'),
        nullable=False, unique=True)

    deceased_workers = Column(Text, nullable=False)  # погибшие
    severely_injured_workers = Column(
        Text, nullable=False)  # тяжело травмированные
    # групповые несчастные случаи
    group_accidents = Column(Text, nullable=False)
    workers_with_simple_injuries = Column(
        Text, nullable=False)  # легкие травмы
    workers_with_micro_injuries = Column(Text, nullable=False)  # микротравмы

    passport = orm.relationship('Passport', lazy='select')
