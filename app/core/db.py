from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings, INVISTED_AMOUNT_DEAFUL


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session


class BaseModel(Base):

    __abstract__ = True

    full_amount = Column(
        Integer, CheckConstraint("full_amount >= 1")
    )
    invested_amount = Column(
        Integer,
        CheckConstraint("full_amount >= invested_amount"),
        default=INVISTED_AMOUNT_DEAFUL
    )
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime, default=None)

    def invested(self):
        self.fully_invested = True
        self.close_date = datetime.now()
        self.invested_amount = self.full_amount
