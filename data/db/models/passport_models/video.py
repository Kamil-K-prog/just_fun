from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from ...sqlalchemy_base_maker import SqlAlchemyBase


class Video(SqlAlchemyBase, SerializerMixin):
    ("""Сущность видео (доступного по определённому URL в Rutube), """
     """прикрепляемого к паспорту""")
    __tablename__ = 'video'

    serialize_only = ('id', 'passport_id', 'link')

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    # id паспорта организации, к которому прикреплено видео
    passport_id = Column(Integer, ForeignKey('passport.id'), nullable=False)

    link = Column(Text, unique=True, nullable=False)  # ссылка на web-страницу

    # Связи many-to-one:
    passport = orm.relationship('Passport', lazy='select')
