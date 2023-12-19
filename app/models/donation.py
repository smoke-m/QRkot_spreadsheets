from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.db import BaseModel


class Donation(BaseModel):

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text,)
    charity_projects = relationship('DonatsInProjs', backref='donation')
