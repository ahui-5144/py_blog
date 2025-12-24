from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.v1.endpoints import redis_example, sys_user, article
from core.config import config
from core.cors import setup_cors
from core.database import create_tables, shutdown_db
from core.redis import init_redis, close_redis


# ------------- 创建生命周期
# 应用启动时创建数据库连接池并创建全部的表
# 应用关闭时关闭数据库连接池
'''
asynccontextmanager：用于定义异步上下文管理器，实现应用的启动/关闭逻辑。
'''
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
'''
app = FastAPI(dependencies=[Depends(get_query_token)], lifespan=lifespan) 
    就是所有路由自动注入 get_query_token  类似全局拦截器 强制校验所有接口token（可通过覆盖排除个别路由）
    
app = FastAPI(
    lifespan=lifespan,
    title=config.APP_NAME,
    description="FastAPI Blog API",
    version="1.0.0"
)
    无全局认证，需要逐个路由添加    
'''
app = FastAPI(
    lifespan=lifespan,
    title=config.APP_NAME,
    description="FastAPI Blog API",
    version="1.0.0"
)

# 配置CORS
'''
setup_cors(app)：启用跨域支持，允许前端访问（类似于 Spring WebMvcConfigurer.addCorsMappings()）。
'''
setup_cors(app)

'''
app.include_router(...)：集成用户和 Redis 示例路由（类似于 Spring @Controller 扫描）。
'''
app.include_router(sys_user.router)
app.include_router(redis_example.router)

app.include_router(article.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=28000)