import sys
from fastapi import APIRouter
import requests as res
import json
from fastapi import Form,Header
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
from typing import List
import random
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

logger = logging.getLogger(__name__)

class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> Dysmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = f'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

def check_phone_number(phone_number,re_code):
    if len(phone_number)!= 11:
        return {"code":400,"message":"请输入正确的手机号"}
    else:
        code = ''.join(random.choices('0123456789', k=6))
        client = Sample.create_client(access_key_id='LTAI5tNVqQ16EgH2Xn6fxar1',
                                      access_key_secret='eIm61r1Uy8e5IDjDepBN3JKiqXmLeO')
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name='闲猫MewStore',
            template_code='SMS_460685295',
            phone_numbers=phone_number,
            template_param='{"code":"%s"}' % code
        )
        runtime = util_models.RuntimeOptions()
        response = client.send_sms_with_options(send_sms_request, runtime)
        if response.body.code == 'OK':
            datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
            logger.debug('发送验证码成功')
            return {"code": 200, "message": '发送成功'}
        else:
            return {"code": 400, "message": '发送失败'}
    if re_code != code:
        return{"code":400,"message":"验证码错误"}
    else:
        return{"code":200,"message":"success"}
