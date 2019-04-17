from sqlalchemy import BigInteger, Column, String, text, DateTime, Integer
from app import db


class OTP(db.Model):

    IS_VERIFIED_TRUE = '1'
    IS_VERIFIED_FALSE = '2'

    __tablename__ = "otp"

    id = Column(BigInteger, primary_key=True)
    mobile = Column(String(10))
    otp = Column(String(10))
    is_verified = Column(Integer, server_default=text('2'))
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


