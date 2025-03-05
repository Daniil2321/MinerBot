from .database import async_engine, Requests

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class BaseDAO:
    model = None

    @classmethod
    async def create(cls, **kwargs):
        async with AsyncSession(async_engine) as session:
            async with session.begin():
                instance = cls.model(**kwargs)  # Используем атрибут класса
                session.add(instance)
            # После коммита объект будет в состоянии "detached"
            return instance

    @classmethod
    async def select_one_or_none(cls, **kwargs):
        async with AsyncSession(async_engine) as session:
            async with session.begin():
                query = select(cls.model).filter_by(**kwargs)
                result = await session.execute(query)
                return result.scalar_one_or_none()

    @classmethod
    async def select_all_or_none(cls, **kwargs):
        async with AsyncSession(async_engine) as session:
            async with session.begin():
                query = select(cls.model)
                if kwargs:
                    query = query.filter_by(**kwargs)
                result = await session.execute(query)
                items = result.scalars().all()
                return items if items else None


class RequestsDAO(BaseDAO):
    model = Requests
