from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import orm

from ...sqlalchemy_base_maker import SqlAlchemyBase


class WorkCondition(SqlAlchemyBase):
    """Условия труда в организации"""
    __tablename__ = 'work_condition'

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    passport_id = Column(
        Integer, ForeignKey('passport.id'),
        nullable=False, unique=True)

    # Численность работников, получающих бесплатно CИЗ
    workers_with_free_things = Column(Integer, nullable=False)
    # средний процент обеспеченности
    average_percent_with_things = Column(Integer)

    # Численность работников, получающих бесплатно смывающие ср-ва
    workers_with_free_soap = Column(Integer, nullable=False)
    # средний процент обеспеченности
    average_percent_with_soap = Column(Integer)

    # Численность работников, получающих бесплатно медосмотр
    workers_with_free_medicine = Column(Integer, nullable=False)
    # средний процент работников, прошедших медосмотр
    average_percent_with_medicine = Column(Integer)

    passport = orm.relationship('Passport', lazy='select')
