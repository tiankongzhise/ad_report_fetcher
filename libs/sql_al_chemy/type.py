from typing import TypeVar
from sqlalchemy.orm import DeclarativeBase

SQL_TABLE_MODEL = TypeVar('SQL_TABLE_MODEL',bound=DeclarativeBase)