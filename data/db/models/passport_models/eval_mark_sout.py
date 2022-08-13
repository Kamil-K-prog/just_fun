from sqlalchemy import Column, Integer, Text
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from ...sqlalchemy_base_maker import SqlAlchemyBase
from ...db_utils import versatile_represent, versatile_convert_to_str
from config import AppConfig


class EvalMarkSout(SqlAlchemyBase, SerializerMixin):
    """Метка качества и наличия специальной оценки условий труда (СОУТ)"""
    __tablename__ = 'eval_mark_sout'
    __table_args__ = AppConfig.DB_TABLE_ARGS

    serialize_only = ('id', 'title')

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    # Наименование метки качества
    # при id=1 => title='да'
    # при id=2 - title='нет'
    # при id=3 - title='частично'
    title = Column(Text, nullable=False)

    # Связи one-to-many:
    passports = orm.relationship('Passport', lazy='select')

    __repr__ = versatile_represent

    __str__ = versatile_convert_to_str
