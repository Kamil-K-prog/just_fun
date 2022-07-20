from sqlalchemy import Column, Integer, Text

from ...sqlalchemy_base_maker import SqlAlchemyBase


class PassportStatus(SqlAlchemyBase):
    ("""Статус паспорта в рамках процесса его регистрации в системе. """
     """По типу: 1 - 'Принят', 2 - 'На рассмотрении', 3 - 'Отклонен'""")
    __tablename__ = 'passport_status'

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    name = Column(Text, unique=True, nullable=False)  # Наименование статуса
