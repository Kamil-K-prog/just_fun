from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy import orm

from ...sqlalchemy_base_maker import SqlAlchemyBase


class CollectiveAgreement(SqlAlchemyBase):
    """Сущность коллективного договора"""
    __tablename__ = 'collective_agreement'

    id = Column(
        Integer,
        primary_key=True, nullable=False,
        autoincrement=True, unique=True)

    passport_id = Column(Integer, ForeignKey('passport.id'), nullable=False)

    # Наличие профсоюзной организации
    is_union_organization = Column(Boolean, nullable=False, default=False)
    # Номер уведомительной регистрации коллективного договора
    # (NULL при отсутствии коллективного договора)
    notificational_registration_number = Column(Integer, nullable=True)
    # Номер уведомительной регистрации при наличии изменений в колдоговоре
    # (NULL при отсутствии изменений в колдоговоре)
    is_agreement_changes = Column(Integer, nullable=True)

    passport = orm.relationship('Passport', lazy='select')
