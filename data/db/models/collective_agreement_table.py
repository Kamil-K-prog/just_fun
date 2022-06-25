from sqlalchemy import Column, Integer, Text, ForeignKey, Boolean
from sqlalchemy import orm
from .SqlAlchemyBase_maker import SqlAlchemyBase



class CollectiveAgreement(SqlAlchemyBase):
    __tablename__ = 'collective_agreement'

    passport_id = Column(Integer, ForeignKey('passports.id'), primary_key=True, nullable=False, autoincrement=True,
                         unique=True)  # id паспорта
    is_union_organization = Column(Boolean)  # Наличие профсоюзной организации
    is_collective_agreement = Column(Text, default='0')  # Наличие коллективного договора (если да, то №)
    is_agreement_changes = Column(Text, default='0')  # Изменения в колдоговор(если да, то №)

    passport = orm.relation('Passport')
