from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import BaseModel


class Donation(BaseModel):

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text,)
