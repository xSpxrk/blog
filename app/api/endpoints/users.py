from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.encoders import jsonable_encoder
from app.db.db import database
from app import schemas, models
from app.core import security
from typing import List
from app import crud
from app.api import deps
from databases import Database

from pydantic import EmailStr

router = APIRouter()


@router.get('/', response_model=List[schemas.User])
async def get_users(
        skip: int = 0,
        limit: int = 20,
        db: Database = Depends(deps.get_db)
):
    users = await crud.user.get_multi(db=db, skip=skip, limit=limit)
    return users


@router.post('/', response_model=schemas.User)
async def create_user(
        user_in: schemas.UserCreate
):
    user = await crud.user.get_by_email(database, user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail='Пользователь с такой электронной почтой существует'
        )
    user = await crud.user.create(database, user_in)
    return user


@router.get("/me", response_model=schemas.User)
async def get_user_me(
        current_user: models.User = Depends(deps.get_current_user)
):
    return current_user


@router.put('/me', response_model=schemas.User)
async def update_user_me(
        db: Database = Depends(deps.get_db),
        password: str = Body(None),
        username: str = Body(None),
        email: EmailStr = Body(None),
        current_user: models.User = Depends(deps.get_current_user)
):
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.hashed_password = security.get_password_hash(password)
    if username is not None:
        user_in.username = username
    if email is not None:
        user_in.email = email
    user = await crud.user.update(db=db, id=current_user.id, value=user_in)
    return user


@router.get('/{user_id}', response_model=schemas.User)
async def get_user_by_id(
        user_id: int
):
    user = await crud.user.get(database, user_id)
    return user
