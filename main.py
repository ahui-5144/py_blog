from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.v1.endpoints import redis_example, users, heroes, items
from core.database import create_tables, shutdown_db
from core.redis import init_redis, close_redis


# ------------- 创建生命周期
# 应用启动时创建数据库连接池并创建全部的表
# 应用关闭时关闭数据库连接池
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 在连接实例中获取数据库连接
    # 创建数据库连接池并创建全部的表
    await create_tables()
    
    # 初始化Redis连接
    await init_redis()

    yield   # 此时fastapi开始运行

    # 关闭数据库链接
    await shutdown_db()
    
    # 关闭Redis连接
    await close_redis()

# lifespan 是 FastAPI 应用的生命周期管理函数，用于在应用启动和关闭时执行一些操作。
# 这里的 lifespan 函数会在应用启动时创建数据库连接池并创建全部的表，在应用关闭时关闭数据库连接池。
# app = FastAPI(dependencies=[Depends(get_query_token)], lifespan=lifespan)
app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(items.router)
app.include_router(heroes.router)
app.include_router(redis_example.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}