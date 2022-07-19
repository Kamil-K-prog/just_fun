from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy import orm

from ...sqlalchemy_base_maker import SqlAlchemyBase


class Sout(SqlAlchemyBase):
    """Специальная оценка условий труда (СОУТ)"""
    __tablename__ = 'sout'

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    passport_id = Column(
        Integer, ForeignKey('passport.id'),
        nullable=False, unique=True)

    # Пройдена ли специальная оценка
    # 1 - да
    # 2 - нет
    # 3 - частично
    special_test = Column(Integer, nullable=False)

    report_date = Column(Date, nullable=False)  # Дата внесения отчета СОУТ
    # Номер отчета во ФГИС СОУТ
    report_number = Column(Integer, nullable=False)

    # Всего рабочих мест в организации
    jobs_all_count = Column(Integer, nullable=False)
    # Количество рабочих мест, на которых проведена СОУТ
    jobs_with_sout = Column(Integer, nullable=False)
    # % рабочих мест, охваченных СОУТ
    # (отношение от общего количества)
    jobs_with_sout_percent = Column(Integer, nullable=False)

    # Количество рабочих мест с условиями труда (сколько единиц)
    jobs_with_work_conditions = Column(Integer, nullable=False)
    # Кол-во человек, занятых на рабочих мест с условиями труда (сколько чел.)
    jobs_with_work_conditions_and_workers = Column(Integer, nullable=True)

    class1 = Column(Integer, nullable=False)  # класс 1
    class2 = Column(Integer, nullable=False)  # класс 2
    class31 = Column(Integer, nullable=False)  # класс 3.1
    class32 = Column(Integer, nullable=False)  # класс 3.2
    class33 = Column(Integer, nullable=False)  # класс 3.3
    class34 = Column(Integer, nullable=False)  # класс 3.4
    class4 = Column(Integer, nullable=False)  # класс 4

    # % работников, занятых на работах с вредными и (или) опасными
    # условиями труда от общего количества работников организации
    workers_with_dangerous_work_percent = Column(Integer, nullable=False)

    passport = orm.relationship('Passport', lazy='select')
