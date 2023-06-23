import logging
from random import random
import requests as res
import json
import uvicorn
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Form, requests,Header
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, BigInteger, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel as PydanticBaseModel

Base = declarative_base()
engine = create_engine('mysql://mew_store:114514@106.14.35.23:3306/test', echo=True)
# engine = create_engine('mysql://root:123456@127.0.0.1:3306/mewfish', echo=True)
Session = sessionmaker(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

print("数据库连接成功")

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    nickname = Column(String(50))
    username = Column(String(50))
    profile_photo = Column(String(50))
    password = Column(String(102))
    phone_number = Column(String(11))
    money = Column(DECIMAL(20, 2))
    status = Column(Integer)
    name = Column(String(50))
    id_card = Column(String(18))

class Good(Base):
    __tablename__ = "good"
    id = Column(BigInteger, primary_key=True)
    view = Column(Integer)
    game = Column(String(50))
    title = Column(String(50))
    content = Column(Text)
    picture = Column(Text)
    account = Column(String(50))
    password = Column(String(50))
    status = Column(Integer)  # 商品状态未审核为0，审核通过为1，审核不通过为-1,被下架为2，已售出为3
    seller_id = Column(BigInteger)
    price = Column(DECIMAL(10, 2))


app = FastAPI()

logger = logging.getLogger(__name__)
class Login(BaseModel):
    username: str
    password: str


class ItemQuery(BaseModel):
    page: int = 1
    size: int = 4