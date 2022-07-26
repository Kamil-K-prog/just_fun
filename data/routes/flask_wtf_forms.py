from typing import List
import datetime

from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, DateField, \
    IntegerField, FileField, SelectField
from wtforms import EmailField, StringField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange


from ..db.db_preparation_manager import LOCATIONS, EVAL_MARK_CONTENTS


class NullableDateField(DateField):
    ("""Поле даты, которое может вернуть None, если дата не заполнена, """
     """не выбрасывая ошибку""")

    def process_formdata(self, valuelist: List[str]) -> None:
        if valuelist:
            date_str = ' '.join(valuelist).strip()
            if not date_str:
                self.data = None
                return None

            try:
                self.data = datetime.datetime.strptime(
                    date_str, '%Y-%m-%d').date()
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid date value'))


class LoginForm(FlaskForm):
    """Форма авторизации"""
    login = StringField("Логин:",
                        validators=[DataRequired(),
                                    Length(min=2, max=25)])
    password = PasswordField(
        "Пароль:", validators=[DataRequired(),
                               Length(min=5, max=25)])
    remember_me = BooleanField("Запомнить меня:")
    submit = SubmitField("Вход")


class RegisterForm(FlaskForm):
    """Форма регистрации пользователя"""
    login = StringField("Логин:",
                        validators=[DataRequired()])
    email = EmailField("Почта:", validators=[DataRequired()])
    password = PasswordField(
        "Пароль:",
        [
            DataRequired(),
            EqualTo("confirm", message="Пароли должны соответствовать"),
            Length(min=5, max=25)
        ],
    )
    confirm = PasswordField("Повторите пароль:")
    submit = SubmitField("Зарегистрироваться")


class PassportForm(FlaskForm):
    """Форма добавления/редактирования паспорта"""

    name_of_the_legal_entity = StringField(
        "Наименование ОПФ юрлица", validators=[DataRequired()])
    organization_full_name = StringField(
        "Полное наименование организации (для ИП - ФИО)",
        validators=[DataRequired()])
    organization_short_name = StringField(
        "Краткое наименование организации (для ИП - ФИО)",
        validators=[DataRequired()])

    boss_surname = StringField(
        "Фамилия руководителя", validators=[DataRequired()])
    boss_name = StringField("Имя руководителя", validators=[DataRequired()])
    boss_patronymic = StringField(
        "Отчество руководителя", validators=[DataRequired()])

    boss_position = StringField("Должность руководителя",
                                validators=[DataRequired()])

    phone_number = StringField(
        "Телефон организации", validators=[DataRequired()])
    email_oficcial = StringField(
        "Email организации официальный", validators=[DataRequired()])
    location = SelectField(
        "Населенный пункт/примерное местоположение",
        validators=[DataRequired()],
        choices=[(loc, loc) for loc in LOCATIONS])

    fact_address = StringField(
        "Фактический адрес", validators=[DataRequired()])
    legal_address = StringField(
        "Юридический адрес", validators=[DataRequired()])

    INN = StringField("ИНН", validators=[DataRequired()])
    OKTMO = StringField("ОКТМО", validators=[DataRequired()])
    main_activity_OKVED = StringField(
        "Основной вид деятельности по ОКВЭД", validators=[DataRequired()])

    male_workers_count = IntegerField(
        'Колличество мужчин', validators=[NumberRange(min=0)], default=0)
    female_workers_count = IntegerField(
        'Колличество женщин', validators=[NumberRange(min=0)], default=0)

    workers_protector_surname = StringField(
        "Фамилия специалиста по охране труда", validators=[DataRequired()])
    workers_protector_name = StringField(
        "Имя специалиста по охране труда", validators=[DataRequired()])
    workers_protector_patronymic = StringField(
        "Отчество специалиста по охране труда", validators=[DataRequired()])
    workers_protector_position = StringField(
        "Должность специалиста по охране труда", validators=[DataRequired()])
    workers_protector_phone_number = StringField(
        "Телефон специалиста по охране труда", validators=[DataRequired()])
    workers_protector_email = StringField(
        "E-mail специалиста по охране труда", validators=[DataRequired()])

    sout_check = SelectField(
        "Пройдена ли специальная оценка СОУТ",
        validators=[DataRequired()],
        choices=[(emark, emark) for emark in EVAL_MARK_CONTENTS])

    sout_report_date = NullableDateField("Дата внесения отчета СОУТ")

    sout_report_number = StringField("Номер отчета во ФГИС СОУТ")

    jobs_all_count = IntegerField(
        "Всего рабочих мест в организации", validators=[
            NumberRange(min=0)], default=0)

    jobs_with_sout = IntegerField(
        "Количество рабочих мест, на которых проведена СОУТ", validators=[
            NumberRange(min=0)], default=0)

    jobs_with_sout_percent = IntegerField(
        "Процент рабочих мест, охваченных СОУТ",
        validators=[NumberRange(min=0)], default=0)

    jobs_with_work_conditions = IntegerField(
        "Количество рабочих мест с условиями труда",
        validators=[NumberRange(min=0)], default=0)

    jobs_with_work_conditions_and_workers = IntegerField(
        "Кол-во человек, занятых на рабочих местах с условиями труда",
        validators=[NumberRange(min=0)], default=0)

    sout_danger_class1 = IntegerField(
        "Количество работников, имеющих класс опасности 1",
        validators=[NumberRange(min=0)], default=0)

    sout_danger_class2 = IntegerField(
        "Количество работников, имеющих класс опасности 2",
        validators=[NumberRange(min=0)], default=0)

    sout_danger_class31 = IntegerField(
        "Количество работников, имеющих класс опасности 3.1",
        validators=[NumberRange(min=0)], default=0)

    sout_danger_class32 = IntegerField(
        "Количество работников, имеющих класс опасности 3.2",
        validators=[NumberRange(min=0)], default=0)

    sout_danger_class33 = IntegerField(
        "Количество работников, имеющих класс опасности 3.3",
        validators=[NumberRange(min=0)], default=0)

    sout_danger_class34 = IntegerField(
        "Количество работников, имеющих класс опасности 3.4",
        validators=[NumberRange(min=0)], default=0)

    sout_danger_class4 = IntegerField(
        "Количество работников, имеющих класс опасности 4",
        validators=[NumberRange(min=0)], default=0)

    workers_with_dangerous_work_percent = IntegerField(
        "Процент работников, занятых на работах с вредными и (или) опасными "
        "условиями труда от общего количества работников организации",
        validators=[NumberRange(min=0)], default=0)

    profrisks_check = SelectField(
        "Проведена оценка профрисков в области охраны труда",
        validators=[DataRequired()],
        choices=[(emark, emark) for emark in EVAL_MARK_CONTENTS])

    last_profrisks_check_date = NullableDateField(
        "Дата проведения последней оценки профрисков")

    workers_with_free_ppe = IntegerField(
        "Численность работников, получающих бесплатно CИЗ",
        validators=[NumberRange(min=0)], default=0)

    average_percent_with_ppe = IntegerField(
        "Средний процент обеспеченности СИЗ",
        validators=[NumberRange(min=0)], default=0)

    workers_with_free_soap = IntegerField(
        "Численность работников, получающих бесплатно смывающие средства",
        validators=[NumberRange(min=0)], default=0)

    average_percent_with_soap = IntegerField(
        "Средний процент обеспеченности смывающими средствами",
        validators=[NumberRange(min=0)], default=0)

    workers_with_free_medicine = IntegerField(
        "Численность работников, получающих бесплатно медосмотр",
        validators=[NumberRange(min=0)], default=0)

    average_percent_with_medicine = IntegerField(
        "Средний процент работников, прошедших медосмотр",
        validators=[NumberRange(min=0)], default=0)

    deceased_workers = IntegerField(
        "Кол-во погибших работников",
        validators=[NumberRange(min=0)], default=0)

    severely_injured_workers = IntegerField(
        "Кол-во тяжело травмированных работников",
        validators=[NumberRange(min=0)], default=0)

    group_accidents = IntegerField(
        "Кол-во групповых несчастных случаев",
        validators=[NumberRange(min=0)], default=0)

    workers_with_simple_injuries = IntegerField(
        "Кол-во работников с лёгкими травмами",
        validators=[NumberRange(min=0)], default=0)

    workers_with_micro_injuries = IntegerField(
        "Кол-во работников с микротравмами",
        validators=[NumberRange(min=0)], default=0)

    have_local_regulatory_act = BooleanField(
        ("Наличие локального нормативного акта, "
         "регламентирующего систему управления охраной труда"),
        default="checked")

    have_commission_of_workers_protection = BooleanField(
        "Наличие комитета по охране труда", default="checked")

    trusted_persons_for_protection = IntegerField(
        "Количество уполномоченных лиц по охране труда",
        validators=[NumberRange(min=0)], default=0)

    have_agreement_on_work_protection = BooleanField(
        "Наличие соглашения по охране труда в организации",
        default="checked")

    have_office_of_work_protection = BooleanField(
        "Наличие кабинета (уголка) охраны труда", default="checked")

    have_room_for_medical_care = BooleanField(
        "Наличие помещения для оказания медицинской помощи",
        default="checked")

    have_improve_working_conditions_plan = BooleanField(
        "Наличие плана мероприятий по улучшению и оздоровлению условий труда",
        default="checked")

    the_amount_of_financing = IntegerField(
        "Объем финансирования этого плана (тыс. рублей)",
        validators=[NumberRange(min=0)], default=0)

    have_employees_health_save_plan = BooleanField(
        "Наличие корпоративной программы сохранения здоровья работников",
        default="checked")

    workers_to_train_count = IntegerField(
        ("Количество работников, которые должны проходить обучение по "
         "охране труда и проверку знаний требований охраны труда в "
         "аккредитованных образовательных организациях"),
        validators=[NumberRange(min=0)], default=0)

    trained_workers = IntegerField(
        "Процент фактически прошедших такое обучение",
        validators=[NumberRange(min=0)], default=0)

    is_timely_training = BooleanField(
        "Своевременное проведение инструктажей по охране труда",
        default="checked")

    have_union_organization = BooleanField(
        "Наличие профсоюзной организации",
        default="checked")

    have_collective_agreement = BooleanField(
        "Наличие коллективного договора", default="checked")

    notificational_registration_number = StringField(
        "Номер уведомительной регистрации коллективного договора")

    notificational_registration_number_with_changes = StringField(
        "Номер уведомительной регистрации при наличии изменений в колдоговоре")

    submit = SubmitField("Отправить")


class GetFilesForm(FlaskForm):
    photo = FileField('Поддерживаемые форматы: jpeg, jpg, png, gif')

    video_url = StringField(
        "Проверьте ссылку на работоспособность перед отправкой")

    submit = SubmitField("Отправить")


class AdminAddForm(FlaskForm):
    name = StringField('Название:', validators=[DataRequired()])
    submit = SubmitField("Создать")


class GoldenBadgeApplicationForm(FlaskForm):
    organization_id = IntegerField(
        'ID организации, для которой подается заявка',
        validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Отправить')
