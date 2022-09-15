from typing import Generic, TypeVar, Type
from sqlalchemy import Table
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from databases import Database

ModelType = TypeVar('ModelType', bound=Table)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: Database, id: int):
        query = self.model.select().where(self.model.c.id == id)
        return await db.fetch_one(query)

    async def get_multi(self, db: Database, skip: int = 0, limit: int = 20):
        query = self.model.select().offset(skip).limit(limit)
        return await db.fetch_all(query)

    async def create(self, db: Database, value: CreateSchemaType):
        obj_data: dict = jsonable_encoder(value)
        query = self.model.insert().values(obj_data)
        return await db.execute(query=query)

    async def update(self, db: Database, id: int, value: UpdateSchemaType):
        obj_data: dict = jsonable_encoder(value)
        query = self.model.update().where(self.model.c.id == id).values(obj_data)
        await db.execute(query)
        return await self.get(db=db, id=id)

    async def remove(self, db: Database, id: int):
        query = self.model.delete().where(self.model.c.id == id)
        return await db.execute(query)

