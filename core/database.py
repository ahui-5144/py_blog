from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, close_all_sessions
from sqlalchemy.ext.declarative import declarative_base

from .config import config
from .logger import app_logger

# 创建异步引擎
engine = create_async_engine(
    config.SQLALCHEMY_DATABASE_URL,
    echo=config.DEBUG,  # 打印SQL语句，开发环境下可以设置为True，便于调试
    # 连接池配置
    pool_size=config.DB_POOL_SIZE,  # 连接池大小
    max_overflow=config.DB_MAX_OVERFLOW,  # 连接池溢出的最大连接数
    pool_timeout=config.DB_POOL_TIMEOUT,  # 获取连接的超时时间（秒）
    pool_recycle=config.DB_POOL_RECYCLE,  # 连接回收时间（秒），防止连接超时
    pool_pre_ping=config.DB_POOL_PRE_PING  # 在使用连接前检查连接是否有效
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
        app_logger.info('数据库连接成功，已创建全部表')
    except Exception as e:
        app_logger.error(f"数据库连接失败：{e}")
        raise e

async def shutdown_db():
    """关闭所有连接并释放引擎"""
    try:
        # 1. 先关掉还在使用的会话
        await close_all_sessions()
        # 2. 再关掉引擎（连接池）
        await engine.dispose()
        app_logger.info("数据库连接池已释放")
    except Exception as e:
        app_logger.error(f"关闭数据库连接失败：{e}")
