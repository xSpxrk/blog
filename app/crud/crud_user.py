from .base import CRUDBase
from app.models import User
from app.schemas import UserCreate, UserUpdate
from databases import Database
from fastapi.encoders import jsonable_encoder
from app.core.security import get_password_hash, verify_password
from typing import Optional


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    async def create(self, db: Database, value: UserCreate):
        obj = jsonable_encoder(value)
        obj['hashed_password'] = get_password_hash(obj['password'])
        del obj['password']
        query = self.model.insert()
        user_id = await db.execute(query=query, values=obj)
        return await self.get(db, user_id)

    async def get_by_email(self, db: Database, email: str) -> User:
        query = self.model.select().where(self.model.c.email == email)
        return await db.fetch_one(query)

    async def authenticate(self, db: Database, email: str, password: str) -> User:
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


user = CRUDUser(User)
