from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.core.config import MAX_NAME_LENGTH, MIN_ANYSTR_LENGTH


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=MAX_NAME_LENGTH)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        min_anystr_length = MIN_ANYSTR_LENGTH
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: Annotated[str, Field(max_length=MAX_NAME_LENGTH,)]
    description: Annotated[str, Field()]
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    pass
