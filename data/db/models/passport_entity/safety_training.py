from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy import orm

from ...sqlalchemy_base_maker import SqlAlchemyBase


class SafetyTraining(SqlAlchemyBase):
    __tablename__ = 'safety_training'

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    passport_id = Column(
        Integer, ForeignKey('passport.id'),
        nullable=False, unique=True)

    # Количество работников, которые должны проходить обучение по охране
    # труда и проверку знаний требований охраны труда в аккредитованных
    # образовательных организациях
    workers_count = Column(Integer)
    # процент фактически прошедших такое обучение
    trained_workers = Column(Integer)
    # Своевременное проведение инструктажей по охране труда (да/нет)
    timely_training = Column(Boolean, nullable=False, default=False)

    passport = orm.relationship('Passport', lazy='select')
