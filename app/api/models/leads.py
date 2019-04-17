from sqlalchemy import BigInteger, ForeignKey, DateTime, String, Column, Text, text, Integer
from app import db
from sqlalchemy.orm import relationship


class Lead(db.Model):

    APPROVED = '1'
    REJECTED = '2'
    IS_DELETED_TRUE = '1'
    IS_DELETED_FALSE = '2'

    __tablename__ = "leads"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    title = Column(String(255))
    lead_description = Column(Text)
    category = Column(String(255))
    sub_category = Column(String(255))
    price = Column(String(255))
    tag = Column(String(255))
    score = Column(String(244))
    features = Column(String(255))
    status = Column(Integer, nullable=False, server_default=text("'2'"))
    is_deleted = Column(Integer, nullable=False, server_default=text("'2'"))
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = relationship('User', uselist=False, lazy="joined")

