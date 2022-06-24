from string import ascii_letters, printable, digits
from wtforms.validators import ValidationError


invalid_combinations = [
    "qwe",
    "ert",
    "wer",
    "rty",
    "tyu",
    "yui",
    "uio",
    "iop",
    "asd",
    "sdf",
    "dfg",
    "fgh",
    "ghj",
    "hjk",
    "jkl",
    "zxc",
    "xcv",
    "cvb",
    "vbn",
    "bnm",
    "йцу",
    "цук",
    "уке",
    "кен",
    "енг",
    "нгш",
    "гшщ",
    "шщз",
    "щзх",
    "зхъ",
    "фыв",
    "ыва",
    "вап",
    "апр",
    "про",
    "рол",
    "олд",
    "лдж",
    "джэ",
    "ячс",
    "чсм",
    "сми",
    "мит",
    "ить",
    "тьб",
    "ьбю",
    "жэё",
]


class NameValidator:
    def __init__(self, min_len=2, max_len=25):
        self.min_len = min_len
        self.max_len = max_len

    def __call__(self, form, field):
        if not field.data.isalpha():
            raise ValidationError(
                message="Имя, Фамилия, Отчество должны состоять только из букв"
            )
        if self.min_len > len(field.data) >= self.max_len:
            raise ValidationError(
                message="Имя, Фамилия, Отчество должны иметь длинну от {self.min_len} до {self.max_len}"
            )


class LoginValidator:
    def __init__(self, min_len=2, max_len=25):
        self.min_len = min_len
        self.max_len = max_len
        self.valid_symb = ascii_letters + digits + "-_"

    def __call__(self, form, field):
        if self.min_len > len(field.data) >= self.max_len:
            raise ValidationError(
                message="Логин должен иметь длинну от {self.min_len} до {self.max_len}"
            )
        for i in field.data.strip():
            if i not in self.valid_symb:
                raise ValidationError(
                    message="Логин должен содержать тоьлко буквы, цифры и символы: -_"
                )


class PasswordValidator:
    def __init__(self, min_len=8, max_len=25):
        self.min_len = min_len
        self.max_len = max_len
        self.valid_symb = printable

    def __call__(self, form, field):
        if self.min_len > len(field.data) >= self.max_len:
            raise ValidationError(
                message="Пароль должен иметь длинну от {self.min_len} до {self.max_len}"
            )
        if field.data.lower() == field.data or field.data.upper() == field.data:
            raise ValidationError(
                message="Пароль должен содержать строчные и заглавные буквы"
            )
        if not any([c in field.data for c in list(digits)]):
            raise ValidationError(message="Пароль должен содержать цифры")
        if any([i in field.data.lower() for i in invalid_combinations]):
            raise ValidationError(
                message="Пароль не долен содержать комбинации из подряд идущих символов"
            )
        for i in field.data.strip():
            if i not in self.valid_symb:
                raise ValidationError(message="Пароль содержит недопустимые символы")
