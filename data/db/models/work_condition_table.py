from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase


# таблица для "Управление профрисками"

class WorkCondition(SqlAlchemyBase):
    __tablename__ = 'work_conditions'

    passport_id = Column(Integer, ForeignKey('passports.id'), primary_key=True, nullable=False, autoincrement=True,
                         unique=True)  # id организации

    workers_with_free_things = Column(Integer, nullable=False)  # Численность работников, получающих бесплатно CИЗ
    average_percent_with_things = Column(Integer)  # средний процент обеспеченности

    workers_with_free_soap = Column(Integer,
                                    nullable=False)  # Численность работников, получающих бесплатно смывающие ср-ва
    average_percent_with_soap = Column(Integer)  # средний процент обеспеченности

    workers_with_free_medicine = Column(Integer,
                                        nullable=False)  # Численность работников, получающих бесплатно медосмотр
    average_percent_with_medicine = Column(Integer)  # средний процент работников, прошедших медосмотр

    passport = orm.relation('Passport')
