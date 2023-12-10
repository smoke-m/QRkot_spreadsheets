from sqlalchemy import Column, String, Text

from app.core.config import MAX_NAME_LENGTH
from app.core.db import BaseModel


class CharityProject(BaseModel):

    name = Column(String(MAX_NAME_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)
