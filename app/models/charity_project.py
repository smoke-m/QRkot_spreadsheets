from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.core.config import MAX_NAME_LENGTH
from app.core.db import BaseModel


class CharityProject(BaseModel):

    name = Column(String(MAX_NAME_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    donatoins = relationship(
        'DonatsInProjs', backref='charityproject', cascade='delete'
    )
