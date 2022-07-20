from sqlalchemy import Column, Integer, ForeignKey, Text, Date
from sqlalchemy import orm

from ...sqlalchemy_base_maker import SqlAlchemyBase
from ...db_utils import get_current_yekt_datetime
from config import AppConfig


LAZY = AppConfig.ORM_MODEL_RELATIONSHIP_LAZY_PARAM


class UserLog(SqlAlchemyBase):
    """Сущность события, связанного с пользователем, в журнале приложения"""
    __tablename__ = 'user_log'

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    # Суть произошедшего события в текстовом виде
    # (или часть фразы, описывающей суть)
    info = Column(Text, nullable=False)

    date = Column(  # дата и время протекания события
        Date, nullable=False,
        default=get_current_yekt_datetime)

    user = orm.relationship('User', lazy=LAZY)
