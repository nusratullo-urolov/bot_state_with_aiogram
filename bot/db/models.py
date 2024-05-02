import enum

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, BigInteger
from sqlalchemy.orm import relationship, Mapped

from bot.db.base import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    address: Mapped[list['Address']] = relationship(back_populates='user', lazy='selectin')
    language: Mapped[list['Language']] = relationship(back_populates='user', lazy='selectin')


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    longitude = Column(Float())
    latitude = Column(Float())
    user_id = Column(BigInteger, ForeignKey('user.id', ondelete='CASCADE'))
    user: Mapped['User'] = relationship(back_populates='address')



class Language(Base):
    __tablename__ = 'language'
    id = Column(Integer, primary_key=True)

    class Status(enum.Enum):
        uz = 'uz'
        en = "en"
        ru = "ru"

    language = Column(Enum(Status), server_default=Status.uz.name)
    user_id = Column(BigInteger, ForeignKey('user.id', ondelete='CASCADE'), unique=True)
    user: Mapped['User'] = relationship(back_populates='language')
