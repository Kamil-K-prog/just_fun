from sqlalchemy import Column, Integer, ForeignKey, Text, Date
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from ...sqlalchemy_base_maker import SqlAlchemyBase
from ...db_utils import get_current_yekt_datetime
from config import AppConfig


LAZY = AppConfig.ORM_MODEL_RELATIONSHIP_LAZY_PARAM


class PassportLog(SqlAlchemyBase, SerializerMixin):
    ("""Сущность события, связанного с паспортом организации, """
     """в журнале приложения""")
    __tablename__ = 'passport_log'

    serialize_only = ('id', 'passport_id', 'info', 'date')

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    passport_id = Column(Integer, ForeignKey('passport.id'), nullable=False)

    # Суть произошедшего события в текстовом виде
    # (или часть фразы, описывающей суть)
    info = Column(Text, nullable=False)

    date = Column(  # дата и время протекания события
        Date, nullable=False,
        default=get_current_yekt_datetime)

    passport = orm.relationship('Passport', lazy=LAZY)
