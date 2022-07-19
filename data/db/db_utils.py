import datetime


def get_current_yekt_datetime() -> datetime.datetime:
    ("""Возвращает объект datetime, содержащий текущее время """
     """в временной зоне Екатеринбурга (YEKT)""")
    return datetime.datetime.utcnow() + datetime.timedelta(hours=5)
