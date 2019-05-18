from sqlalchemy import ForeignKey, BigInteger, text, Column, DateTime
from app import db
from sqlalchemy.orm import relationship


class LeadSales(db.Model):

    __tablename__ = "lead_sales"

    id = Column(BigInteger, primary_key=True)
    lead_id = Column(BigInteger, ForeignKey('leads.id'), nullable=False)
    buyer_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    seller_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = relationship('User', foreign_keys="[LeadSales.buyer_id]", uselist=False, lazy="joined")
    lead = relationship('Lead', uselist=False, lazy="joined")
