from datetime import datetime
from sqlalchemy import Column, DateTime, MetaData, func, Integer, String, BOOLEAN, LargeBinary
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

# Создаем асинхронный движок для PostgreSQL (asyncpg)
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/MinerBot"
async_engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base(metadata=MetaData())


class BaseClass(Base):
    __abstract__ = True

    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class Requests(BaseClass):
    __tablename__ = "Requests"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    file = Column(LargeBinary, nullable=True)
    is_done = Column(BOOLEAN, server_default="0")
