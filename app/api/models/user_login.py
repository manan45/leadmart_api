from sqlalchemy import BigInteger, Text, Integer, text, DateTime, Column, text
from app import db


class UserLogin(db.Model):

    IS_ACTIVE_TRUE = '1'
    IS_ACTIVE_FALSE = '2'

    __tablename__ = "user_login"

    id = Column(BigInteger, primary_key=True)
    token = Column(Text)
    user_id = Column(BigInteger())
    user_type = Column(Integer)
    is_active = Column(Integer, nullable=False, server_default=text("'0'"))
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

