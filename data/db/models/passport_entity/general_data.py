from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy import orm

from ...sqlalchemy_base_maker import SqlAlchemyBase


class GeneralData(SqlAlchemyBase):
    """Модель с информацией из секции 'Общие данные' паспорта организации"""
    __tablename__ = 'general_data'

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    passport_id = Column(
        Integer, ForeignKey('passport.id'),
        nullable=False, unique=True)

    # Наличие локального нормативного акта, регламентирующего систему
    # управления охраной труда
    local_regulatory_act = Column(Boolean, nullable=False, default=False)
    # Наличие комитета (комиссии) по охране труда
    commission_of_workers_protection = Column(
        Boolean, nullable=False, default=False)
    # Количество уполномоченных (доверенных) лиц по охране труда
    trusted_persons_for_protection = Column(Integer, default=0)
    # Наличие соглашения по охране труда в организации
    agreement_on_work_protection = Column(
        Boolean, nullable=False, default=False)
    # Наличие кабинета (уголка) охраны труда
    office_of_work_protection = Column(Boolean, nullable=False, default=False)
    # Наличие помещения для оказания медицинской помощи
    room_for_medical_care = Column(Boolean, nullable=False, default=False)
    # Наличие плана мероприятий по улучшению и оздоровлению условий труда
    improve_working_conditions_plan = Column(
        Boolean, nullable=False, default=False)
    # объем финансирования этого плана (тыс. рублей)
    the_amount_of_financing = Column(Integer, nullable=False, default=0)
    # Наличие корпоративной программы сохранения здоровья работников
    employees_health_save_plan = Column(Boolean, nullable=False, default=False)

    passport = orm.relationship('Passport', lazy='select')
