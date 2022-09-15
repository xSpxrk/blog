from fastapi import FastAPI
from app.db.db import database
from app.api.endpoints import users, login
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


app.include_router(users.router, prefix='/users', tags=['users'])
app.include_router(login.router, tags=['login'])
