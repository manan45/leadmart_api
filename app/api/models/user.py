from sqlalchemy import BigInteger, Column, DateTime, Integer, String, text
from app import db


class User(db.Model):

    IS_BLOCKED_TRUE = '1'
    IS_BLOCKED_FALSE = '2'

    TYPE = {
        'admin': '1',
        'user': '2',
        'super_admin': '3'
    }

    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(255))
    surname = Column(String(255))
    email = Column(String(255), nullable=False, server_default=text("''"))
    mobile = Column(String(10))
    type = Column(Integer, nullable=False, server_default=text("'2'"))
    username = Column(String(255), nullable=False, server_default=text("''"))
    password = Column(String(512))
    is_blocked = Column(Integer, nullable=False, server_default=text("'2'"))
    company_name = Column(String(255))
    designation = Column(String(255))
    facebook = Column(String(255))
    twitter = Column(String(255))
    linkedin = Column(String(255))
    instagram = Column(String(255))
    address = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    country = Column(String(255))
    # TODO  profile picture
    profile_picture = Column(String(255), server_default=text('"not now"'))
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    is_authenticated = True

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type
