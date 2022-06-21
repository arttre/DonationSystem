from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, DECIMAL, SMALLINT
from sqlalchemy.orm import relationship

from .db import Base, engine


class Users(Base):
    __tablename__ = 'Users'

    UserID = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    Email = Column(String(255), unique=True, nullable=False)
    PhoneNumber = Column(String(13), unique=True)
    FirstName = Column(String(255), nullable=False)
    LastName = Column(String(255), nullable=False)
    Password = Column(String(255), nullable=False)

    users = relationship('UserRoles', back_populates='user', cascade='all, delete', passive_deletes=True)

    fund_request = relationship('FundRequests', back_populates='recipient', cascade='all, delete', passive_deletes=True)
    donation_request = relationship('DonationRequests', back_populates='benefactor',
                                    cascade='all, delete', passive_deletes=True)


class Roles(Base):
    __tablename__ = 'Roles'

    RoleID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    RoleName = Column(String(255), unique=True, nullable=False)

    roles = relationship('UserRoles', back_populates='role', cascade='all, delete', passive_deletes=True)


class UserRoles(Base):
    __tablename__ = 'UserRoles'

    UserRoleID = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    Role = Column(Integer, ForeignKey('Roles.RoleID', ondelete='CASCADE'), primary_key=True)
    User = Column(BigInteger, ForeignKey('Users.UserID', ondelete='CASCADE'), primary_key=True)

    role = relationship('Roles', back_populates='roles')
    user = relationship('Users', back_populates='users')


class FundRequests(Base):
    __tablename__ = 'FundRequests'

    RequestID = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    StartAmount = Column(DECIMAL(18, 2), nullable=False)
    CurrentAmount = Column(DECIMAL(18, 2), nullable=False)
    Recipient = Column(BigInteger, ForeignKey('Users.UserID', ondelete='CASCADE'), nullable=False)
    Motivation = Column(String(255), nullable=False)
    IBAN = Column(String(34), nullable=False)
    Status = Column(SMALLINT)

    recipient = relationship('Users', back_populates='fund_request')

    donation_request = relationship('DonationRequests', back_populates='fund_request',
                                    cascade='all, delete', passive_deletes=True)

    need_fund_request = relationship('NeedFundRequests', back_populates='fund_request',
                                     cascade='all, delete', passive_deletes=True)


class DonationRequests(Base):
    __tablename__ = 'DonationRequests'

    DonationID = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    Amount = Column(DECIMAL(18, 2), nullable=False)
    Benefactor = Column(BigInteger, ForeignKey('Users.UserID', ondelete='CASCADE'), nullable=False)
    FundRequest = Column(BigInteger, ForeignKey('FundRequests.RequestID', ondelete='CASCADE'), nullable=False)
    Message = Column(String(255))
    Status = Column(SMALLINT)

    benefactor = relationship('Users', back_populates='donation_request')
    fund_request = relationship('FundRequests', back_populates='donation_request')


class Needs(Base):
    __tablename__ = 'Needs'

    NeedID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    NeedName = Column(String(255), unique=True, nullable=False)

    need_fund_request = relationship('NeedFundRequests', back_populates='need',
                                     cascade='all, delete', passive_deletes=True)


class NeedFundRequests(Base):
    __tablename__ = 'NeedFundRequests'

    NeedFundRequestID = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    Need = Column(Integer, ForeignKey('Needs.NeedID', ondelete='CASCADE'), primary_key=True)
    FundRequest = Column(BigInteger, ForeignKey('FundRequests.RequestID', ondelete='CASCADE'), primary_key=True)

    need = relationship('Needs', back_populates='need_fund_request')
    fund_request = relationship('FundRequests', back_populates='need_fund_request')


Base.metadata.create_all(engine)

