from sqlalchemy import Column, Integer, Text, ForeignKey, Boolean
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase


class GeneralData(SqlAlchemyBase):
    __tablename__ = 'general_data'

    passport_id = Column(Integer, ForeignKey('passports.id'), primary_key=True, nullable=False, autoincrement=True,
                         unique=True)  # id паспорта
    local_regulatory_act = Column(Boolean)  # локальный нормативный акт
    commission_of_workers_protection = Column(Boolean)  # комиссия по охране труда
    trusted_persons_for_protection = Column(Boolean)  # уполномоченные лица по охране труда
    agreement_on_work_protection = Column(Boolean)  # соглашение по охране труда
    office_of_work_protection = Column(Boolean)  # кабинет охраны труда
    room_for_medical_care = Column(Boolean)  # помещение для мед. помощи
    improve_working_conditions_plan = Column(Boolean)  # план по улучшению условий труда
    the_amount_of_financing = Column(Integer)  # объем финансирования этого плана (тыс. рублей)
    employees_health_save_plan = Column(Boolean)  # корпоративная программа сохранения здоровья работников

    passport = orm.relation('Passport')
