from sqlalchemy import Column, Integer, Text

from ...sqlalchemy_base_maker import SqlAlchemyBase


class EvalMark(SqlAlchemyBase):
    ("""Метка качества и наличия проведения оценок """
     """соблюдения каких-либо государственных стандартов. """
     """Например, оценка СОУТ или оценка профрисков в организации""")
    __tablename__ = 'eval_mark'

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    # Наименовании метки качества
    # при id=1 => title='да'
    # при id=2 - title='нет'
    # при id=3 - title='частично'
    title = Column(Text, nullable=False)
