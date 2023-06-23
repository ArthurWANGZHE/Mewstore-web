from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import List
from fastapi import APIRouter
from fastapi import Form, Header, File,UploadFile
import jwt
from utils.data import User
from datetime import datetime
import logging
import random
from fastapi import FastAPI, WebSocket, APIRouter
from typing import List
from pydantic import BaseModel
from utils.globals import Session, SECRET_KEY, EXPIRATION_DELTA
router = APIRouter()

# 存储连接的客户端 WebSocket
connected_clients = []

# 存储聊天记录
chat_history = []


class Message(BaseModel):
    sender_id: int
    receiver_id: int
    message: str


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket,authorization: str = Header(...)):
    session = Session()
    token = authorization
    payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
    user = session.query(User).filter(User.id == payload['id']).first()
    if user:
        await websocket.accept()
        connected_clients.append(websocket)

        try:
            while True:
                data = await websocket.receive_json()
                message = Message(**data)
                chat_history.append(message)
                await broadcast(message)
        except Exception:
            connected_clients.remove(websocket)


async def broadcast(message: Message):
    for client in connected_clients:
        await client.send_json(message.dict())


@router.get("/connected-clients", response_model=List[int])
async def get_connected_clients():
    return [id(client) for client in connected_clients]


class Message:
    def __init__(self, send_id: int, message: str, message_id: int, message_type: str, send_time: datetime):
        self.send_id = send_id
        self.message = message
        self.message_id = message_id
        self.message_type = message_type
        self.send_time = send_time


@router.get("/message-history")
async def get_message_history(receive_id: int, send_id: int, message_history=None, message_type=None):
    # 查询数据库中的历史记录
    receive_history = [message for message in message_history if
                       message.send_id == send_id and message_type.is_read == 1]
    send_history = [message for message in message_history if
                    message.send_id == receive_id and message_type.is_read == 1]
    message_history = list(set(receive_history + send_history))  # 去重
    message_history = sorted(message_history, key=lambda x: x.send_time)  # 按照时间排序
    message_list = []
    # 添加消息到列表中
    for message in message_history:
        message_dict = {
            'send_id': str(message.send_id),
            'message': message.message,
            'message_id': str(message.message_id),
            'type': message.message_type,
            'send_time': message.send_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        message_list.append(message_dict)

    if not message_list:
        return JSONResponse({'code': 400, 'message': '暂无历史消息'}, status_code=400)

    return JSONResponse({'code': 200, 'message': '获取成功', 'data': message_list}, status_code=200)

