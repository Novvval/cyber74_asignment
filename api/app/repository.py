import contextlib
from typing import Type, TypeVar, Any, Sequence

from sqlalchemy import select, delete, Row, RowMapping
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, Load

from .models import BaseModel, Product, Price
from db import Database

SQLAlchemyOptions = TypeVar('SQLAlchemyOptions', Load, list[Load], tuple[Load, ...])


class Repository:
    def __init__(self, db):
        self.db: Database = db
        self.session: AsyncSession = None

    @contextlib.asynccontextmanager
    async def session_context(self):
        async with self.db.session() as session:
            self.session = session
            try:
                yield
                await self.session.commit()
            except SQLAlchemyError:
                await self.session.rollback()
            finally:
                await self.session.close()
                self.session = None


    async def add(self, obj: BaseModel | list[BaseModel]) -> BaseModel:
            if isinstance(obj, list):
                self.session.add_all(obj)
                await self.session.flush()
            else:
                self.session.add(obj)
                await self.session.flush()

            return obj


    async def get_many(
            self, model: Type[BaseModel],
            query: bool = None,
            options: SQLAlchemyOptions = None,
            limit: int = None,
            offset: int = None
    ) -> Sequence[Row[Any] | RowMapping | Any]:

        stmnt = select(model)
        if options is not None:
            stmnt = stmnt.options(options)
        if query is not None:
            stmnt = query.where(query)
        if limit is not None:
            stmnt = stmnt.limit(limit)
        if offset is not None:
            stmnt = stmnt.offset(offset)
        result = await self.session.execute(stmnt)
        return result.unique().scalars().all()


    async def get_one(
            self,
            model: Type[BaseModel],
            query: bool,
            options: SQLAlchemyOptions = None
    ) -> BaseModel | None:

        stmnt = select(model)
        if options is not None:
            stmnt = stmnt.options(options)
        stmnt = stmnt.where(query)
        result = await self.session.execute(stmnt)
        result =  result.unique().scalars().first()
        return result


    async def delete(self, obj: BaseModel | list[BaseModel]) -> None:
            await self.session.delete(obj)


    async def delete_many(
            self, model: Type[BaseModel],
            query: bool = None,
            options: SQLAlchemyOptions = None
    ) -> None:

        stmnt = delete(model)
        if options is not None:
            stmnt = stmnt.options(options)
        query = stmnt.where(query)
        await self.session.execute(query)


    async def get_prices(self, query: bool = None) -> Sequence[Row[Any] | RowMapping | Any]:
        stmt = select(Price).join(Product).where(query).options(joinedload(Price.product))
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()