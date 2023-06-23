from fastapi import APIRouter
from fastapi import Form, Header, File,UploadFile
import datetime
import jwt
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.security import generate_password_hash, check_password_hash
from utils.check_name import r_n_a
from utils.sendsms import check_phone_number
from utils.snowflake import id_generate
from utils.UploadQiNiu import uploadFile
from utils.data import User
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


# 注册用户
@router.post("/register")
async def register(username: str = Form(...),
                   password: str = Form(...),
                   re_password: str = Form(...),
                   phone_number: str = Form(...),
                   re_code: str = Form(...)):
    session = Session()
    if password != re_password:
        return {"code": 400, "message": "两次密码不一致"}
    if check_phone_number(phone_number, re_code)["code"] == "400":
        return {"code": 400, "message": "验证码错误"}
    else:
        password = generate_password_hash(password)
        id = id_generate(1, 1)
        user1 = User()
        user1.id = id
        user1.username = username
        user1.password = password
        user1.phone_number = phone_number
        user1.status = 0
        session.add(user1)
        session.commit()
        session.close()
        return {"code": 200, "message": "success"}


# 登录
@router.post("/login")
async def login(password: str = Form(...),
                username: str = Form(...),
                ):
    session = Session()
    user = session.query(User).filter(User.username == username).first()
    if check_password_hash(user.password, password):
        payload = {'exp': datetime.datetime.utcnow() + EXPIRATION_DELTA,
                   'id': user.id, 'status': user.status}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return {'token': token, "code": 200, "message": "登录成功"}
    else:
        return {"code": 400, "message": "登录失败"}


# 更新密码
@router.patch("/update_password")
async def update_password(password: str = Form(...),
                          new_password: str = Form(...),
                          authorization: str = Header(...)):
    session = Session()
    token = authorization
    payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
    user = session.query(User).filter(User.id == payload['id']).first()
    if check_password_hash(user.password, password):
        user.password = generate_password_hash(new_password)
        session.commit()
    session.close()
    return {"code": 200, "message": "修改成功"}


# 实名认证
@router.post("/checkname")
async def checkname(name: str = Form(...),
                    id_card: str = Form(...),
                    authorization: str = Header(...)):
    session = Session()
    token = authorization
    payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
    user = session.query(User).filter(User.id == payload['id']).first()
    if user:
        if r_n_a(name, id_card):
            user.name = name
            session.commit()
            return {"code": 200, "message": "success"}
        else:
            return {"code": 400, "message": "fail"}
    else:
        return {"code": 400, "message": "not found"}
    session.close()


# 更新昵称
@router.patch("/nickname")
async def update_nickname(nickname: str = Form(...),
                          authorization: str = Header(...)):
    session = Session()
    token = authorization
    payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
    user = session.query(User).filter(User.id == payload['id']).first()
    if user:
        user.nickname = nickname
        session.commit()
        session.close()
        return {"code": 200, "message": "修改成功"}
    else:
        return {"code": 400, "message": "修改失败"}


# 更新头像
"""
@router.patch("/profile_photo", response_model=None)
async def update_profile_photo(profile_photo: FileStorage = File(...), authorization: str = Header(...)):
    session = Session()
    token = authorization
    payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
    user = session.query(User).filter(User.id == payload['id']).first()
    if user:
        user.profile_photo = UploadFile(profile_photo.file)
        session.commit()
        session.close()
        return {"code": 200, "message": "修改头像成功"}
    else:
        return {"code": 400, "message": "修改头像失败"}
"""

# 氪金
@router.patch("/money")
async def update_money(money: float = Form(...),
                       authorization: str = Header(...)):
    session = Session()
    token = authorization
    payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
    user = session.query(User).filter(User.id == payload['id']).first()
    if user:
        user.money = money
        session.commit()
        session.close()
        return {"code": 200, "message": "充值成功"}
    else:
        return {"code": 400, "message": "充值失败"}
