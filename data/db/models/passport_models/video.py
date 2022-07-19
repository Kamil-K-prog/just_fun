from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy import orm

from ...sqlalchemy_base_maker import SqlAlchemyBase


class Video(SqlAlchemyBase):
    __tablename__ = 'video'

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    # id паспорта организации, к которому прикреплён файл
    passport_id = Column(Integer, ForeignKey('passport.id'))
    link = Column(Text, unique=True, nullable=True)  # ссылка на web-страницу

    # Связи meny-to-one:
    passport = orm.relationship('Passport', lazy='select')
