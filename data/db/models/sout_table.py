from sqlalchemy import Column, Integer, Text, ForeignKey, Date
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase


# таблица для "Специальная оценка условий труда (СОУТ)"

class Sout(SqlAlchemyBase):
    __tablename__ = 'souts'

    passport_id = Column(Integer, ForeignKey('passports.id'), primary_key=True, nullable=False, autoincrement=True,
                             unique=True)  # id организации
    special_test = Column(Integer, nullable=False)  # Специальная оценка проведена да/нет/частично

    report_date = Column(Date, nullable=False)  # Дата внесения отчета СОУТ и
    report_number = Column(Text, nullable=False)  # Номер отчета во ФГИС СОУТ

    jobs_all_count = Column(Integer, nullable=False)  # Всего рабочих мест в организации
    jobs_with_sout = Column(Integer, nullable=False)  # Количество рабочих мест, на которых проведена СОУТ
    jobs_with_sout_percent = Column(Integer, nullable=False)  # % рабочих мест, охваченных СОУТ
    # (отношение от общего количества)

    jobs_with_work_conditions = Column(Integer, nullable=False)  # Количество рабочих мест с условиями труда, ед.
    jobs_with_work_conditions_and_workers = Column(Integer, nullable=True)  #
    class1 = Column(Integer, nullable=False)  # класс 1
    class2 = Column(Integer, nullable=False)  # класс 2
    class31 = Column(Integer, nullable=False)  # класс 3.1
    class32 = Column(Integer, nullable=False)  # класс 3.2
    class33 = Column(Integer, nullable=False)  # класс 3.3
    class34 = Column(Integer, nullable=False)  # класс 3.4
    class4 = Column(Integer, nullable=False)  # класс 4

    workers_with_dangerous_work_percent = Column(Integer, nullable=False)  # % работников, занятых на работах с вредными
    # и (или) опасными условиями труда от общего количества работников организации

    passport = orm.relation('Passport')
