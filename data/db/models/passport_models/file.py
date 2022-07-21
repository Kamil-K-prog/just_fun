from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from ...sqlalchemy_base_maker import SqlAlchemyBase


class File(SqlAlchemyBase, SerializerMixin):
    ("""Модель c информацией о файлах (в файловой системе сервера), """
     """прикрепляемых к паспорту. Прежде всего, для фотографий""")
    __tablename__ = 'file'

    serialize_only = ('id', 'passport_id', 'filename')

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    # id паспорта организации, к которому прикреплён файл
    passport_id = Column(Integer, ForeignKey('passport.id'), nullable=False)

    filename = Column(Text, unique=True, nullable=False)

    # Связи many-to-one:
    passport = orm.relationship('Passport', lazy='select')
