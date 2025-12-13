import redis.asyncio as redis
from contextlib import asynccontextmanager

from .config import config
from .logger import app_logger

# 创建Redis连接池
redis_pool = redis.ConnectionPool(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    password=config.REDIS_PASSWORD,
    decode_responses=True,  # 自动解码响应为字符串
    max_connections=config.REDIS_MAX_CONNECTIONS,  # 连接池最大连接数
)

# 创建Redis客户端实例
redis_client = redis.Redis(connection_pool=redis_pool)


@asynccontextmanager
async def get_redis():
    """
    获取Redis连接的依赖函数
    使用示例:
    async with get_redis() as redis_conn:
        await redis_conn.set("key", "value")
        value = await redis_conn.get("key")
    """
    try:
        yield redis_client
    except Exception as e:
        # 记录错误日志
        app_logger.error(f"Redis操作出错: {e}")
        raise
    finally:
        # 注意：这里不需要手动关闭连接，因为使用的是连接池
        pass


async def close_redis():
    """关闭Redis连接池"""
    try:
        await redis_client.close()
        await redis_pool.disconnect()
        app_logger.info("Redis连接池已关闭")
    except Exception as e:
        app_logger.error(f"关闭Redis连接失败: {e}")


# 初始化函数，用于测试连接
async def init_redis():
    """初始化Redis连接，测试连接是否正常"""
    try:
        await redis_client.ping()
        app_logger.info("Redis连接成功")
        return True
    except Exception as e:
        app_logger.error(f"Redis连接失败: {e}")
        return False