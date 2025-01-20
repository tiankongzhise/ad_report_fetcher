import os
import json
import  dotenv

from sqlalchemy import Column,String,Integer,DateTime,Text,Boolean,DECIMAL,JSON, URL,UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy.schema import MetaData





dotenv.load_dotenv()


# 从环境变量中读取配置
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# 数据库配置
OAUTH_DATABASE_URL = URL.create(
    "mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database="baidudb",
)


engine = create_engine(
    OAUTH_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=3600,
    json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False),
    json_deserializer=lambda obj: json.loads(obj),
)

oauth_session = Session(engine)


class Base(DeclarativeBase):
    def to_dict(self):
        # 获取对象的字典表示
        result = {c.key: getattr(self, c.key)
                  for c in self.__table__.columns}
        return result


class OauthTable(Base):
    __tablename__ = 'bd_auth_token'

    key = Column(Integer, autoincrement=True, nullable=False, default=None, primary_key=True, index=True)
    appId = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    authCode = Column(Text(collation='utf8mb4_0900_ai_ci'))
    secretKey = Column(String(64, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    grantType = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    userName = Column(String(64, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    userId = Column(String(32, collation='utf8mb4_0900_ai_ci'), nullable=True, default='')
    refreshToken = Column(Text(collation='utf8mb4_0900_ai_ci'))
    accessToken = Column(Text(collation='utf8mb4_0900_ai_ci'))
    bdccAccountDict = Column(JSON, nullable=True)
    expiresTime = Column(DateTime, nullable=True)
    refreshExpiresTime = Column(DateTime, nullable=True)
    tableUpdateTime = Column(DateTime, default=None)

    __table_args__ = (
        UniqueConstraint('userId', name='idx_only'),
    )



metadata_obj = MetaData()
metadata_obj.create_all(engine)