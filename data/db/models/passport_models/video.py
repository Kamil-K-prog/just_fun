from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy import orm

from ...sqlalchemy_base_maker import SqlAlchemyBase


class Video(SqlAlchemyBase):
    ("""Сущность видео (доступного по определённому URL в Rutube), """
     """прикрепляемого к паспорту""")
    __tablename__ = 'video'

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    # id паспорта организации, к которому прикреплено видео
    passport_id = Column(Integer, ForeignKey('passport.id'))

    link = Column(Text, unique=True, nullable=False)  # ссылка на web-страницу

    # Связи many-to-one:
    passport = orm.relationship('Passport', lazy='select')
