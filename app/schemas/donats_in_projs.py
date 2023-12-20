from pydantic import BaseModel, Extra, PositiveInt


class DonatsInProjsGet(BaseModel):
    donat: PositiveInt
    charity_project: str

    class Config:
        extra = Extra.forbid
        orm_mode = True
