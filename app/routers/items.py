from fastapi import APIRouter
import requests as res
import json
from fastapi import Form, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
import requests as res
import json
from fastapi import Form, Header, File
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import jwt
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models

import uvicorn
from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List
from datetime import datetime
import logging
import random

from utils.UploadQiNiu import uploadFile
from utils.check_name import r_n_a
from utils.sendsms import Sample, check_phone_number
from utils.snowflake import id_generate
import qiniu
from utils.data import User, Good
import uvicorn
from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List
from datetime import datetime
import logging
import random
from utils.globals import Session, SECRET_KEY, EXPIRATION_DELTA

router = APIRouter()



@router.get("/items")
async def get_items(authorization: str = Header(...)):
    session = Session()
    page = 1
    size = 4
    token = authorization
    payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
    user = session.query(User).filter(User.id == payload['id']).first()

    if user:
        items = session.execute(
            select(Good.id, Good.view, Good.game, Good.title, Good.content, Good.picture, Good.account, Good.password,)
            .where(Good.status == 1)
            .offset((page - 1) * size)
            .limit(size)
        ).all()
    else:
        items = []

    session.close()

    return {"code": 200, "message": "success", "data": items}


@router.get("/itemsquerykeyword")
async def get_itemsquerykeyword(keyword: str = Form(...),
                         authorization: str = Header(...)):
    session = Session()
    token = authorization
    payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
    user = session.query(User).filter(User.id == payload['id']).first()
    if user:
        items = session.execute(
            select(Good.id, Good.view, Good.game, Good.title, Good.content, Good.picture, Good.account, Good.password,)
            .where(Good.status == 1)
            .where(Good.title.like('%' + keyword + '%'))
        ).all()
        if items:
            return {"code": 200, "message": "success", "data": items}
        else:
            return {"code": 400, "message": "not found"}
    else:
        return {"code": 400, "message": "not found"}


@router.get("/itemsquerystauts")
async def get_itemsquerystauts(status: int= Form(...),
                         authorization: str = Header(...)):
    session = Session()
    token = authorization
    payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
    user = session.query(User).filter(User.id == payload['id']).first()
    if user:
        items = session.execute(
            select(Good.id, Good.view, Good.game, Good.title, Good.content, Good.picture, Good.account, Good.password,)
            .where(Good.status == status)
        ).all()
        if items:
            return {"code": 200, "message": "success", "data": items}
        else:
            return {"code": 400, "message": "not found"}
    else:
        return {"code": 400, "message": "not found"}


@router.get("/itemsqueryself")
async def get_itemsqueryself(
                         authorization: str = Header(...)):
    session = Session()
    token = authorization
    payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
    user = session.query(User).filter(User.id == payload['id']).first()
    if user:
        items = session.execute(
            select(Good.id, Good.view, Good.game, Good.title, Good.content, Good.picture, Good.account, Good.password,)
            .where(Good.status == 1)
            .where(Good.seller_id == user.id)
        ).all()
        if items:
            return {"code": 200, "message": "success", "data": items}
        else:
            return {"code": 400, "message": "not found"}
    else:
        return {"code": 400, "message": "not found"}