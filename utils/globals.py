from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

SECRET_KEY = "mewstore"
EXPIRATION_DELTA = datetime.timedelta(days=1)
websocket_ip = 'localhost'

Base = declarative_base()
engine = create_engine('mysql://mew_store:114514@106.14.35.23:3306/test', echo=True)
# engine = create_engine('mysql://root:123456@127.0.0.1:3306/mewfish', echo=True)
Session = sessionmaker(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")