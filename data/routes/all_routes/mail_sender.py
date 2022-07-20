import smtplib

from ...db.db_utils import get_current_yekt_datetime
from config import AppConfig


def log_smtp_exception(smtplib_exception: smtplib.SMTPException) -> None:
    """Логирует ошибки отправки писем"""
    # (на данный момент заглушка - просто печать в стандартный вывод)
    # TODO: сделать реальное логирование, используя модуль logging
    print(f'{smtplib_exception!r} {get_current_yekt_datetime()}')


def send_mail(user: str, mail_to: str, subject: str, text: str) -> None:
    """Отправляет письмо на электронную почту"""
    body = '\r\n'.join((
        f'From: {AppConfig.EMAIL_FROM}',
        f'To: {mail_to}',
        f'Subject: {subject}',
        '',
        f'{user}, {text}'))

    try:
        with smtplib.SMTP(AppConfig.EMAIL_HOST) as smtp_server:
            smtp_server.sendmail(AppConfig.EMAIL_FROM, [mail_to], body)
    except smtplib.SMTPException as smtp_exc:
        log_smtp_exception(smtp_exc)
