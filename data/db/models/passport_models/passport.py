from sqlalchemy import Column, Integer, Text, ForeignKey, Date, Boolean
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from ...sqlalchemy_base_maker import SqlAlchemyBase
from ...db_utils import get_current_yekt_datetime, default_same_as, \
    versatile_represent, versatile_convert_to_str
from config import AppConfig


LAZY = AppConfig.ORM_MODEL_RELATIONSHIP_LAZY_PARAM


class Passport(SqlAlchemyBase, SerializerMixin):
    """Сущность паспорта организации в системе мониторинга"""
    __tablename__ = 'passport'

    serialize_only = (
        'id', 'user_id', 'passport_status_id',
        'date_of_application_submission', 'date_of_application_editing',
        'name_of_the_legal_entity', 'organization_full_name',
        'organization_short_name', 'location', 'legal_address',
        'fact_address', 'boss_surname', 'boss_name', 'boss_patronymic',
        'boss_position', 'INN', 'OKTMO', 'main_activity_OKVED',
        'male_workers_count', 'female_workers_count', 'phone_number',
        'email_oficcial', 'workers_protector_surname',
        'workers_protector_name', 'workers_protector_patronymic',
        'workers_protector_position', 'workers_protector_phone_number',
        'workers_protector_email', 'golden_badge_verdict',
        'golden_badge_application_date', 'golden_badge_verification_date',
        'sout_check_eval_mark_id', 'sout_report_date', 'sout_report_number',
        'jobs_all_count', 'jobs_with_sout', 'jobs_with_sout_percent',
        'jobs_with_work_conditions', 'jobs_with_work_conditions_and_workers',
        'sout_danger_class1', 'sout_danger_class2', 'sout_danger_class31',
        'sout_danger_class32', 'sout_danger_class33', 'sout_danger_class34',
        'sout_danger_class4', 'workers_with_dangerous_work_percent',
        'profrisks_check_eval_mark_id', 'last_profrisks_check_date',
        'workers_with_free_ppe', 'average_percent_with_ppe',
        'workers_with_free_soap', 'average_percent_with_soap',
        'workers_with_free_medicine', 'average_percent_with_medicine',
        'deceased_workers', 'severely_injured_workers', 'group_accidents',
        'workers_with_simple_injuries', 'workers_with_micro_injuries',
        'have_local_regulatory_act', 'have_commission_of_workers_protection',
        'trusted_persons_for_protection', 'have_agreement_on_work_protection',
        'have_office_of_work_protection', 'have_room_for_medical_care',
        'have_improve_working_conditions_plan', 'the_amount_of_financing',
        'have_employees_health_save_plan', 'workers_to_train_count',
        'trained_workers', 'is_timely_training', 'have_union_organization',
        'have_collective_agreement', 'notificational_registration_number',
        'notificational_registration_number_with_changes')

    id = Column(
        Integer, primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    # id пользователя, который зарегистрировал эту организацию
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    # id статуса паспорта этой организации
    # по умолчанию 'Отклонен'
    passport_status_id = Column(Integer, ForeignKey(
        'passport_status.id'), nullable=False, default=3)

    # *** СЕКЦИЯ "Общие сведения" ***

    # дата создания паспорта
    date_of_application_submission = Column(
        Date, nullable=False, default=get_current_yekt_datetime)

    # дата последнего редактирования паспорта
    date_of_application_editing = Column(
        Date, nullable=False, default=get_current_yekt_datetime)

    name_of_the_legal_entity = Column(
        Text, nullable=False)  # Наименование ОПФ юрлица

    # Полное наименование организации, для ИП - ФИО
    organization_full_name = Column(Text, nullable=False, unique=True)

    # Краткое наименование организации
    organization_short_name = Column(Text, nullable=False, unique=True)

    # примерный(обобщённый для поиска) адрес
    location_id = Column(  # По умолчанию Оренбург
        Integer, ForeignKey('location.id'), nullable=False, default=1)

    legal_address = Column(  # Адрес юридический
        Text, nullable=False, unique=True)

    # Адрес фактический
    # по умолчанию совпадает с юридическим адресом
    fact_address = Column(
        Text, nullable=False, unique=True,
        default=default_same_as('legal_address'))

    boss_surname = Column(  # Фамилия руководителя
        Text, nullable=False)

    boss_name = Column(  # Имя руководителя
        Text, nullable=False)

    boss_patronymic = Column(  # Отчество руководителя
        Text, nullable=False)

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

    # Следующие поля описывают специалиста по охране труда
    # или ответственного за охрану труда

    workers_protector_surname = Column(  # Фамилия специалиста по охране труда
        Text, nullable=False)

    workers_protector_name = Column(  # Имя специалиста по охране труда
        Text, nullable=False)

    workers_protector_patronymic = Column(
        Text, nullable=False)  # Отчество специалиста по охране труда

    # должность специалиста по охране труда
    workers_protector_position = Column(Text, nullable=False)

    # телефон специалиста по охране труда
    workers_protector_phone_number = Column(Text, nullable=False)

    # email специалиста по охране труда
    workers_protector_email = Column(Text, nullable=False)

    # "Золотой знак" организации (есть/нет)
    golden_badge_verdict = Column(Boolean, nullable=False, default=False)

    golden_badge_application_date = Column(  # дата подачи заявки на статус
        Date, nullable=True)  # "Золотой знак" (NULL, если пока не подавали)

    # дата подтверждения статуса "Золотой знак"
    golden_badge_verification_date = Column(  # NULL при отстутствии знака
        Date, nullable=True)  # (то есть при golden_badge_verdict == False)

    # *** СЕКЦИЯ "Специальная оценка условий труда (СОУТ)" ***

    # Пройдена ли специальная оценка СОУТ
    # 1 - да
    # 2 - нет
    # 3 - частично
    sout_check_eval_mark_id = Column(
        Integer, ForeignKey('eval_mark_sout.id'),
        nullable=False, default=2)

    # Дата внесения отчета СОУТ
    # NULL, если отчёт СОУТ не вносили
    sout_report_date = Column(Date, nullable=True)

    # Номер отчета во ФГИС СОУТ
    # (Text, т.к. длинный номер может не "влезть" в Integer)
    # NULL, если не имеется номер отчета во ФГИС СОУТ
    sout_report_number = Column(Text, nullable=True)

    # Всего рабочих мест в организации
    jobs_all_count = Column(Integer, nullable=False, default=0)

    # Количество рабочих мест, на которых проведена СОУТ
    jobs_with_sout = Column(Integer, nullable=False, default=0)

    # % рабочих мест, охваченных СОУТ
    # (отношение от общего количества)
    jobs_with_sout_percent = Column(Integer, nullable=False, default=0)

    # Количество рабочих мест с условиями труда (сколько единиц)
    jobs_with_work_conditions = Column(Integer, nullable=False, default=0)

    # Кол-во человек, занятых на рабочих мест с условиями труда (сколько чел.)
    jobs_with_work_conditions_and_workers = Column(
        Integer, nullable=False, default=0)

    # В зависимости от потенциального вреда, который возможен для работника,
    # выделяют 4 класса опасности. Первые 2 класса не опасны для здоровья,
    # вредности 3 класса могут вызвать хронические профессиональные болезни,
    # а 4 класс представляет прямую угрозу жизни.

    # В каждом из следующих полей представлено количество работников,
    # деятельность которых имеет определённый класс/подкласс опасности

    sout_danger_class1 = Column(
        Integer, nullable=False, default=0)  # кол-во у класса 1
    sout_danger_class2 = Column(
        Integer, nullable=False, default=0)  # кол-во у класса 2
    sout_danger_class31 = Column(
        Integer, nullable=False, default=0)  # кол-во у класса 3.1
    sout_danger_class32 = Column(
        Integer, nullable=False, default=0)  # кол-во у класса 3.2
    sout_danger_class33 = Column(
        Integer, nullable=False, default=0)  # кол-во у класса 3.3
    sout_danger_class34 = Column(
        Integer, nullable=False, default=0)  # кол-во у класса 3.4
    sout_danger_class4 = Column(
        Integer, nullable=False, default=0)  # кол-во у класса 4

    # % работников, занятых на работах с вредными и (или) опасными
    # условиями труда от общего количества работников организации
    workers_with_dangerous_work_percent = Column(
        Integer, nullable=False, default=0)

    # *** СЕКЦИЯ "Управление профессиональными рисками" ***

    # Проведена оценка профрисков в области охраны труда
    # 1 - да
    # 2 - нет
    # 3 - частично
    profrisks_check_eval_mark_id = Column(
        Integer, ForeignKey('eval_mark_profrisks.id'),
        nullable=False, default=2)

    # Дата проведения последней оценки профрисков
    last_profrisks_check_date = Column(
        Date, nullable=True)  # NULL, если ещё не проводили

    # *** СЕКЦИЯ "Условия труда" ***

    # Численность работников, получающих бесплатно CИЗ
    # PPE - Personal Protective Equipment (англ. СИЗ)
    workers_with_free_ppe = Column(Integer, nullable=False, default=0)
    # средний процент обеспеченности
    average_percent_with_ppe = Column(Integer, nullable=False, default=0)

    # Численность работников, получающих бесплатно смывающие средства
    workers_with_free_soap = Column(Integer, nullable=False, default=0)
    # средний процент обеспеченности
    average_percent_with_soap = Column(Integer, nullable=False, default=0)

    # Численность работников, получающих бесплатно медосмотр
    workers_with_free_medicine = Column(Integer, nullable=False, default=0)
    # средний процент работников, прошедших медосмотр
    average_percent_with_medicine = Column(Integer, nullable=False, default=0)

    # *** СЕКЦИЯ "Производственный травматизм" ***

    # кол-во погивших работников
    deceased_workers = Column(Integer, nullable=False, default=0)

    # кол-во тяжело травмированных работников
    severely_injured_workers = Column(Integer, nullable=False, default=0)

    # кол-во групповых несчастных случаев
    group_accidents = Column(Integer, nullable=False, default=0)

    # кол-во работников с лёгкими травмами
    workers_with_simple_injuries = Column(Integer, nullable=False, default=0)

    # кол-во работников с микротравмами
    workers_with_micro_injuries = Column(Integer, nullable=False, default=0)

    # *** СЕКЦИЯ "Общие данные" ***

    # Наличие локального нормативного акта, регламентирующего систему
    # управления охраной труда
    have_local_regulatory_act = Column(Boolean, nullable=False, default=False)

    # Наличие комитета (комиссии) по охране труда
    have_commission_of_workers_protection = Column(
        Boolean, nullable=False, default=False)

    # Количество уполномоченных (доверенных) лиц по охране труда
    trusted_persons_for_protection = Column(Integer, nullable=False, default=0)

    # Наличие соглашения по охране труда в организации
    have_agreement_on_work_protection = Column(
        Boolean, nullable=False, default=False)

    # Наличие кабинета (уголка) охраны труда
    have_office_of_work_protection = Column(
        Boolean, nullable=False, default=False)

    # Наличие помещения для оказания медицинской помощи
    have_room_for_medical_care = Column(Boolean, nullable=False, default=False)

    # Наличие плана мероприятий по улучшению и оздоровлению условий труда
    have_improve_working_conditions_plan = Column(
        Boolean, nullable=False, default=False)

    # объем финансирования этого плана (тыс. рублей)
    the_amount_of_financing = Column(Integer, nullable=False, default=0)

    # Наличие корпоративной программы сохранения здоровья работников
    have_employees_health_save_plan = Column(
        Boolean, nullable=False, default=False)

    # *** СЕКЦИЯ "Обучение по охране труда" ***

    # Количество работников, которые должны проходить обучение по охране
    # труда и проверку знаний требований охраны труда в аккредитованных
    # образовательных организациях
    workers_to_train_count = Column(Integer, nullable=False, default=0)

    # процент фактически прошедших такое обучение
    trained_workers = Column(Integer, nullable=False, default=0)

    # Своевременное проведение инструктажей по охране труда (да/нет)
    is_timely_training = Column(Boolean, nullable=False, default=False)

    # *** СЕКЦИЯ "Коллективный договор" ***

    # Наличие профсоюзной организации
    have_union_organization = Column(Boolean, nullable=False, default=False)

    # Наличие коллективного договора
    have_collective_agreement = Column(Boolean, nullable=False, default=False)

    # Номер уведомительной регистрации коллективного договора
    # (NULL при отсутствии коллективного договора)
    notificational_registration_number = Column(Text, nullable=True)

    # Номер уведомительной регистрации при наличии изменений в колдоговоре
    # (NULL при отсутствии изменений в колдоговоре)
    notificational_registration_number_with_changes = Column(
        Text, nullable=True)

    # Связи many-to-one
    status = orm.relationship('PassportStatus', lazy=LAZY)

    user = orm.relationship('User', back_populates='passports', lazy=LAZY)

    location = orm.relationship('Location', lazy=LAZY)

    sout_check_eval_mark = orm.relationship(
        'EvalMarkSout', back_populates='passports', lazy=LAZY)

    profrisks_check_eval_mark = orm.relationship(
        'EvalMarkProfrisks', back_populates='passports', lazy=LAZY)

    # Связи one-to-many:
    files = orm.relationship('File', back_populates='passport', lazy=LAZY)
    videos = orm.relationship('Video', back_populates='passport', lazy=LAZY)

    processes = orm.relationship(
        'Process', back_populates='passport', lazy=LAZY)

    __repr__ = versatile_represent

    __str__ = versatile_convert_to_str
