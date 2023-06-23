from fastapi import FastAPI
from app.routers.users import router as user_router
from app.routers.items import router as item_router
from app.routers.chatroom import router as chatroom_router
import uvicorn

app = FastAPI()
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(item_router, prefix="/item", tags=["item"])
app.include_router(chatroom_router, prefix="/chatroom", tags=["chatroom"])


if __name__ == '__main__':
    uvicorn.run(app=app, host="127.0.0.1", port=3000)
