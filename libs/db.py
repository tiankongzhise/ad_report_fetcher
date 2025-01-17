# -*- coding: utf-8 -*-
import datetime
import os

from sqlmodel import SQLModel, Field,  create_engine
from sqlmodel import Column,Integer,String,Text,JSON,DateTime,UniqueConstraint
import datetime

import dotenv
dotenv.load_dotenv()


# 从环境变量中读取配置
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# 构建认证数据库引擎
oauth_engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/baidudb",
    echo=True
)

class BdAuthToken(SQLModel, table=True):
    __tablename__ = 'bd_auth_token'

    key: int = Field(sa_column=Column(Integer, autoincrement=True, nullable=False,default=None, primary_key=True, index=True))
    appId: str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    authCode: str = Field(sa_column=Column(Text(collation='utf8mb4_0900_ai_ci')))
    secretKey: str = Field(sa_column=Column(String(64, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    grantType: str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    userName: str = Field(sa_column=Column(String(64, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    userId: str = Field(sa_column=Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default=''))
    refreshToken: str = Field(sa_column=Column(Text(collation='utf8mb4_0900_ai_ci')))
    accessToken: str = Field(sa_column=Column(Text(collation='utf8mb4_0900_ai_ci')))
    bdccAccountDict: dict = Field(sa_column=Column(JSON, nullable=True))
    expiresTime: datetime.datetime = Field(sa_column=Column(DateTime, nullable=True))
    refreshExpiresTime: datetime.datetime = Field(sa_column=Column(DateTime, nullable=True))
    tableUpdateTime: datetime.datetime = Field(sa_column=Column(DateTime, default=None, onupdate=lambda: DateTime.utcnow()))

    __table_args__ = (
        UniqueConstraint('userId', name='idx_only'),
    )


# test_engine = create_engine(
#     f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/test_db",
#     echo=True
# )
#
# class TestTable(SQLModel, table=True):
#     __tablename__ = 'test_table'
#     id:int = Field(sa_column=Column(Integer, autoincrement=True, nullable=False,default=None, primary_key=True, index=True))
#     name:str
#     age:int
#     created_at:DateTime
#
#     class Config:
#         arbitrary_types_allowed = True