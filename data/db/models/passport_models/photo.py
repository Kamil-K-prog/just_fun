from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy import orm

from ...sqlalchemy_base_maker import SqlAlchemyBase


class Photo(SqlAlchemyBase):
    __tablename__ = 'photo'

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    # id паспорта организации, к которому прикреплён файл
    passport_id = Column(Integer, ForeignKey('passport.id'))

    filename = Column(Text, unique=True, nullable=False)

    # Связи many-to-one:
    passport = orm.relationship('Passport', lazy='select')
