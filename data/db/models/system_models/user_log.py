from sqlalchemy import Column, Integer, ForeignKey, Text, Date
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from ...sqlalchemy_base_maker import SqlAlchemyBase
from ...db_utils import get_current_yekt_datetime, versatile_represent, \
    versatile_convert_to_str
from config import AppConfig


LAZY = AppConfig.ORM_MODEL_RELATIONSHIP_LAZY_PARAM


class UserLog(SqlAlchemyBase, SerializerMixin):
    """Сущность события, связанного с пользователем, в журнале приложения"""
    __tablename__ = 'user_log'
    __table_args__ = AppConfig.DB_TABLE_ARGS

    serialize_only = ('id', 'user_id', 'info', 'date')

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

    __repr__ = versatile_represent

    __str__ = versatile_convert_to_str
