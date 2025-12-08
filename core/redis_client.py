import redis.asyncio as redis
from contextlib import asynccontextmanager

# Redis连接配置
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None  # 如果没有密码则设为None

# 创建Redis连接池
redis_pool = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    decode_responses=True,  # 自动解码响应为字符串
    max_connections=20,  # 连接池最大连接数
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
        print(f"Redis操作出错: {e}")
        raise
    finally:
        # 注意：这里不需要手动关闭连接，因为使用的是连接池
        pass


async def close_redis():
    """关闭Redis连接池"""
    await redis_client.close()
    await redis_pool.disconnect()
    print("Redis连接池已关闭")


# 初始化函数，用于测试连接
async def init_redis():
    """初始化Redis连接，测试连接是否正常"""
    try:
        await redis_client.ping()
        print("Redis连接成功")
        return True
    except Exception as e:
        print(f"Redis连接失败: {e}")
        return False