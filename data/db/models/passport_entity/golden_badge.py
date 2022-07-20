from sqlalchemy import Column, Integer, ForeignKey, Date, Boolean
from sqlalchemy import orm

from ...sqlalchemy_base_maker import SqlAlchemyBase
from ...db_utils import get_current_yekt_datetime


class GoldenBadge(SqlAlchemyBase):
    """Сущность 'Золотого знака' организации"""
    __tablename__ = 'golden_badge'

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    passport_id = Column(
        Integer, ForeignKey('passport.id'),
        nullable=False, unique=True)

    # Золотой знак организации (есть/нет)
    verdict = Column(Boolean, nullable=False, default=False)

    application_date = Column(  # дата подачи заявки
        Date, nullable=False,
        default=get_current_yekt_datetime)

    verification_date = Column(  # дата подтверждения статуса "Золотой знак"
        Date, nullable=True)  # NULL при отстутствии знака (при verdict=False)

    passport = orm.relationship('Passport', lazy='select')
