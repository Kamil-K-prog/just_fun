from sqlalchemy import Column, Integer, Text, ForeignKey, Boolean, Date
from sqlalchemy import orm

from ...sqlalchemy_base_maker import SqlAlchemyBase
from ...db_utils import get_current_yekt_datetime
from config import AppConfig


LAZY = AppConfig.ORM_MODEL_RELATIONSHIP_LAZY_PARAM


class Passport(SqlAlchemyBase):
    """Общие сведения об организации"""
    __tablename__ = 'passport'

    id = Column(
        Integer, primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    # кто зарегистрировал эту организацию
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    date_of_application_submission = Column(
        Date, nullable=False,  # дата создания паспорта
        default=get_current_yekt_datetime)

    date_of_data_collection = Column(  # дата сбора информации
        Date, nullable=False, default=get_current_yekt_datetime)

    name_of_the_legal_entity = Column(
        Text, nullable=False)  # Наименование ОПФ юрлица

    # Полное наименование организации, для ИП - ФИО
    organization_full_name = Column(Text, nullable=False, unique=True)
    # Краткое наименование организации
    organization_short_name = Column(Text, nullable=False, unique=True)

    address_for_contact = Column(Text, nullable=False)  # контактный адрес
    legal_address = Column(  # Адрес юридический
        Text, nullable=False, unique=True)
    # Адрес фактический
    # при NULL считать совпадающим с юридическим адресом
    fact_address = Column(Text, nullable=True, unique=True)

    boss_full_name = Column(
        Text, nullable=False)  # ФИО руководителя
    # должность руководителя
    boss_position = Column(Text, nullable=False)

    INN = Column(Text, nullable=False, unique=True)  # ИНН
    OKTMO = Column(Text, nullable=False, unique=True)  # ОКТМО
    # Основной вид деятельности по ОКВЭД
    main_activity_OKVED = Column(Text, nullable=False)

    male_workers_count = Column(  # Количество мужчин-работников
        Integer, nullable=False, default=0)
    female_workers_count = Column(  # Количество женщин-работников
        Integer, nullable=False, default=0)

    phone_number = Column(  # телефон организации
        Text, nullable=False, unique=True)
    email_oficcial = Column(  # официальный email организации
        Text, nullable=False, unique=True)

    # ФИО и должность специалиста по охране труда
    # или ответственного за охрану труда
    workers_protector_FIO_n_position = Column(
        Text, nullable=False, unique=True)

    # телефон специалиста по охране труда
    workers_protector_phone_number = Column(Text, nullable=False, unique=True)
    # email специалиста по охране труда
    workers_protector_email = Column(Text, nullable=False, unique=True)

    # Золотой знак организации(есть/нет)
    golden_mark = Column(Boolean, nullable=False, default=False)
    golden_mark_date = Column(  # когда присвоен статус "Золотой знак"
        Date, nullable=True)  # NULL при отстутствии этого статуса

    passport_status_id = Column(Integer, ForeignKey(
        'passport_status.id'), default=3)

    # Связи many-to-one
    status = orm.relationship(
        'PassportStatus', lazy=LAZY)

    user = orm.relationship('User', back_populates='passports', lazy=LAZY)

    # Связи one-to-many:
    photos = orm.relationship('Photo', back_populates='passport', lazy=LAZY)
    videos = orm.relationship('Video', back_populates='passport', lazy=LAZY)

    processes = orm.relationship(
        'Process', back_populates='passport', lazy=LAZY)

    # Связи one-to-one:
    sout = orm.relationship(
        'Sout', back_populates='passport', uselist=False, lazy=LAZY)
    profrisk = orm.relationship(
        'Profrisk', back_populates='passport', uselist=False, lazy=LAZY)
    work_condition = orm.relationship(
        'WorkCondition', back_populates='passport', uselist=False, lazy=LAZY)
    injuries = orm.relationship(
        'Injuries', back_populates='passport', uselist=False, lazy=LAZY)
    general_data = orm.relationship(
        'GeneralData', back_populates='passport', uselist=False, lazy=LAZY)
    safety_training = orm.relationship(
        'SafetyTraining', back_populates='passport', uselist=False, lazy=LAZY)
    collective_agreement = orm.relationship(
        'CollectiveAgreement',
        back_populates='passport',
        uselist=False, lazy=LAZY)
    golden_mark_application = orm.relationship(
        'GoldenMarkApplication',
        back_populates='passport',
        uselist=False, lazy=LAZY)
