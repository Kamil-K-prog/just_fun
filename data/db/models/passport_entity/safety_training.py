from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy import orm

from ...sqlalchemy_base_maker import SqlAlchemyBase


class SafetyTraining(SqlAlchemyBase):
    """Данные по обучению по охране труда"""
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
    workers_count = Column(Integer, nullable=False, default=0)

    # процент фактически прошедших такое обучение
    trained_workers = Column(Integer, nullable=False, default=0)

    # Своевременное проведение инструктажей по охране труда (да/нет)
    timely_training = Column(Boolean, nullable=False, default=False)

    passport = orm.relationship('Passport', lazy='select')
