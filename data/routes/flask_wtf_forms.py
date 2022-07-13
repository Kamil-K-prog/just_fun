from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, DateField, IntegerField, FileField, SelectField
from wtforms import EmailField, StringField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):  # форма авторизации
    login = StringField("Логин:",
                        validators=[DataRequired(),
                                    Length(min=2, max=25)])
    password = PasswordField(
        "Пароль:", validators=[DataRequired(),
                               Length(min=5, max=25)])
    remember_me = BooleanField("Запомнить меня:")
    submit = SubmitField("Вход")


class RegisterForm(FlaskForm):  # форма регистрации пользователя
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


class PassportForm(FlaskForm):  # форма добавления/редактирования паспорта

    opf = StringField("Наименование ОПФ юрлица", validators=[DataRequired()])
    full_name = StringField("Полное наименование организации (для ИП - ФИО)", validators=[DataRequired()])
    short_name = StringField("Краткое наименование организации (для ИП - ФИО)", validators=[DataRequired()])
    information_date = StringField("Дата сбора информации", validators=[DataRequired()])

    boss_fio = StringField("ФИО руководителя", validators=[DataRequired()])
    boss_place = StringField("Должность руководителя", validators=[DataRequired()])

    company_phone = StringField("Телефон", validators=[DataRequired()])
    company_email = StringField("Email", validators=[DataRequired()])
    location = SelectField("Населенный пункт", validators=[DataRequired()],
                           choices=[
                               ('Оренбург', 'Оренбург'),
                               ('Тюмень', 'Тюмень'),
                               ('Орск', 'Орск'),
                               ('Сорочинск', 'Сорочинск'),
                               ('Бугуруслан', 'Бугуруслан'),
                               ('Гай', 'Гай')
                           ])

    address_fact = StringField("Фактический адрес", validators=[DataRequired()])
    address_yur = StringField("Юридический адрес", validators=[DataRequired()])

    inn = StringField("ИНН", validators=[DataRequired()])
    oktmo = StringField("ОКТМО", validators=[DataRequired()])
    main_activity_okved = StringField("Основной вид деятельности по ОКВЭД", validators=[DataRequired()])

    workers_male_count = IntegerField('Колличество мужчин', validators=[DataRequired()])
    workers_female_count = IntegerField('Колличество женщин', validators=[DataRequired()])

    protector_fio = StringField("ФИО", validators=[DataRequired()])
    protector_phone = StringField("Телефон", validators=[DataRequired()])
    protector_email = StringField("Email", validators=[DataRequired()])

    submit = SubmitField("Отправить")

class AdminAddForm(FlaskForm):
    name = StringField('Название:', validators=[DataRequired()])
    submit = SubmitField("Создать")

class GetFilesForm(FlaskForm):
    photo = FileField('Поддерживаемые форматы: jpeg, jpg, png, gif')

    video_url = StringField("Проверьте ссылку на работоспособность перед отправкой")

    submit = SubmitField("Отправить")


class AdminAddForm(FlaskForm):
    name = StringField('Название:', validators=[DataRequired()])
    submit = SubmitField("Создать")


class GoldenBadgeApplicationForm(FlaskForm):
    date_of_application = DateField("Дата подачи заявки")
    organization_id = IntegerField('ID организации, для которой подается заявка')
    submit = SubmitField('Отправить')


class WorkProtectionForm(FlaskForm):
    pasport_id = StringField('Введите ID организации, для которой заполняется форма', validators=[DataRequired()])
    profrisks_check = SelectField('Проведена оценка профессиональных рисков в области охраны труда',
                                  choices=[('Да', 'Да'),
                                           ('Частично', 'Частично'),
                                           ('Нет', 'Нет')
                                           ], validators=[DataRequired()])
    last_check_date = DateField('Дата проведения последней оценки профессиональных рисков', validators=[DataRequired()])
    submit = SubmitField('Отправить')
