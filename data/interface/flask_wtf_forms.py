from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField
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


class AdminAddForm(FlaskForm):
    name = StringField('Название:', validators=[DataRequired()])
    submit = SubmitField("Создать")
