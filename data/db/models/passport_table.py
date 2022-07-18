from email.policy import default
from sqlalchemy import Column, Integer, Text, ForeignKey, Boolean, Date
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase
import datetime


# Общие сведения об организации

class Passport(SqlAlchemyBase):
    __tablename__ = 'passports'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)  # id организации
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # кто зарегистрировал эту организацию
    date_of_application_submission = Column(Text, nullable=False,
                                            default=datetime.datetime.now().strftime(
                                                '%d.%m.%Y'))  # дата создания паспорта

    date_of_data_collection = Column(Text) # дата сбора информации

    name_of_the_legal_entity = Column(Text, nullable=False)  # Наименование ОПФ юрлица

    organization_full_name = Column(Text, nullable=False, unique=True)  # Полное наименование организации, для ИП - ФИО
    organization_short_name = Column(Text, nullable=False, unique=True)  # Краткое наименование организации

    address_for_contact = Column(Text)  # контектный адрес
    legal_address = Column(Text, nullable=False, unique=True)  # Адрес юридический
    fact_address = Column(Text, nullable=True, unique=True)  # Адрес фактический

    boss_full_name = Column(Text, nullable=False, unique=True)  # ФИО руководителя
    boss_position = Column(Text, nullable=False, unique=True)  # должность руководителя

    INN = Column(Text, nullable=False, unique=True)  # ИНН
    OKTMO = Column(Text, nullable=False, unique=True)  # ОКТМО
    main_activity_OKVED = Column(Text, nullable=False, unique=True)  # Основной вид деятельности по ОКВЭД

    male_workers_count = Column(Integer, nullable=False)  # Кол-во мужчин-работников
    female_workers_count = Column(Integer, nullable=False)  # Кол-во женщин-работников

    phone_number = Column(Text, nullable=False, unique=True)  # телефон организации
    email_oficcial = Column(Text, nullable=False, unique=True)  # email организации

    workers_protector_FIO_n_position = Column(Text, nullable=False,
                                              unique=True)  # ФИО и должность специалиста
    # по охране труда или ответственного за охрану труда
    workers_protector_phone_number = Column(Text, nullable=False, unique=True)  # телефон специалиста по охране труда
    workers_protector_email = Column(Text, nullable=False, unique=True)  # email специалиста по охране труда

    golden_mark = Column(Boolean, nullable=False, default=False)  # Золотой знак организации(есть/нет)
    golden_mark_date = Column(Text, nullable=True)  # когда выдан

    passport_status = Column(Integer, ForeignKey('password_statuses.id'), default=3)

    status = orm.relation('PassportStatus')
    user = orm.relation('User')
    photo = orm.relation('Photo', back_populates='passport')
    video = orm.relation('Video', back_populates='passport')
    sout = orm.relation('Sout', back_populates='passport')
    profrisk = orm.relation('Profrisk', back_populates='passport')
    work_conditions = orm.relation('WorkCondition', back_populates='passport')
    injuries = orm.relation('Injuries', back_populates='passport')
    general_data = orm.relation('GeneralData', back_populates='passport')
    safety_training = orm.relation('SafetyTraining', back_populates='passport')
    collective_agreement = orm.relation('CollectiveAgreement', back_populates='passport')
    golden_mark_application = orm.relation('GoldenMarkApplication', back_populates='passport')
    process = orm.relation('Process', back_populates='passport')