from sqlalchemy import Column, Integer, Text, ForeignKey, Boolean
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase


class SafetyTraining(SqlAlchemyBase):
    __tablename__ = 'safety_training'

    passport_id = Column(Integer, ForeignKey('passports.id'), primary_key=True, nullable=False, autoincrement=True,
                         unique=True)  # id паспорта
    workers_count = Column(Integer)  # сколько должны пройти обучение по охране труда
    trained_workers = Column(Integer)  # процент фактически прошедших
    timely_training = Column(Boolean)  # своевременное проведение интсруктажей да/нет

    passport = orm.relation('Passport')
