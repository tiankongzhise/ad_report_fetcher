# -*- coding: utf-8 -*-
import datetime
import os

from sqlmodel import SQLModel, Field,  create_engine
from sqlmodel import Column,Integer,String,Text,JSON,DateTime,UniqueConstraint

import dotenv
dotenv.load_dotenv()


# 从环境变量中读取配置
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# 构建认证数据库引擎
oauth_engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/baidudb"
)

class OauthTable(SQLModel, table=True):
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
    tableUpdateTime: datetime.datetime = Field(sa_column=Column(DateTime, default=None))

    __table_args__ = (
        UniqueConstraint('userId', name='idx_only'),
    )

oceanengine_engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/oceanengine"
)

class OceanAdHourExternalActionTable(SQLModel):
    __tablename__ = 'oceanengine_ad_hour_external_action'
    auto_key: int = Field(sa_column=Column(Integer, autoincrement=True, nullable=False,default=None, primary_key=True, index=True))
