from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from databases import Database

from jose import jwt

from app.core import security
from app import models, schemas, crud
from app.db.db import database

from pydantic import ValidationError


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl='/login/access-token'
)


async def get_db():
    return database


async def get_current_user(
        db: Database = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.user:
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Не удалось проверить учетные данные"
        )
    user = await crud.user.get(db=db, id=token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return user
