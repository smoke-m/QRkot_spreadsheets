from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt

from app.core.config import MIN_ANYSTR_LENGTH


class DonationBase(BaseModel):
    full_amount: Optional[PositiveInt]
    comment: Optional[str]

    class Config:
        min_anystr_length = MIN_ANYSTR_LENGTH
        extra = Extra.forbid


class DonationCreate(DonationBase):
    full_amount: PositiveInt


class DonationDB(DonationCreate):
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
