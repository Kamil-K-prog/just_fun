from sqlalchemy import Column, Integer, ForeignKey, Text, Date
from sqlalchemy import orm

from ...sqlalchemy_base_maker import SqlAlchemyBase
from ...db_utils import get_current_yekt_datetime
from config import AppConfig


LAZY = AppConfig.ORM_MODEL_RELATIONSHIP_LAZY_PARAM


class PassportLog(SqlAlchemyBase):
    ("""Сущность события, связанного с паспортом организации, """
     """в журнале приложения""")
    __tablename__ = 'passport_log'

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

    passport = orm.relationship('User', lazy=LAZY)
