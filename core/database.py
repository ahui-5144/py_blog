from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, close_all_sessions
from sqlalchemy.ext.declarative import declarative_base

# 数据库连接URL
SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://root:200099@127.0.0.1:33061/fastapi_test?charset=utf8mb4"

# 创建异步引擎
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # 打印SQL语句，开发环境下可以设置为True，便于调试
    # 连接池配置
    pool_size=10,  # 连接池大小
    max_overflow=20,  # 连接池溢出的最大连接数
    pool_timeout=30,  # 获取连接的超时时间（秒）
    pool_recycle=3600,  # 连接回收时间（秒），防止连接超时
    pool_pre_ping=True  # 在使用连接前检查连接是否有效
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    future=True
)

# 创建基础模型类
Base = declarative_base()

# 依赖函数：获取数据库会话
@asynccontextmanager
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def create_tables():
    """
    创建全部数据库表
    :return:
    """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"数据库连接失败：{e}")
        raise e
    print('数据库链接成功，已创建全部表')

async def shutdown_db():
    """关闭所有连接并释放引擎"""
    # 1. 先关掉还在使用的会话
    await close_all_sessions()
    # 2. 再关掉引擎（连接池）
    await engine.dispose()
    print("数据库连接池已释放")
