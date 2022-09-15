from sqlalchemy import Column, Integer, String, Table
from app.db.db import metadata

User = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String),
    Column('hashed_password', String),
    Column('email', String)
)
