from fastapi import APIRouter
from core.redis import get_redis

router = APIRouter(prefix="/redis", tags=["redis"])

@router.get("/set/{key}/{value}")
async def set_key_value(key: str, value: str):
    """设置键值对到Redis"""
    async with get_redis() as redis_conn:
        try:
            await redis_conn.set(key, value)
            return {"message": f"Successfully set {key} = {value}"}
        except Exception as e:
            return {"error": f"Failed to set key-value: {str(e)}"}

@router.get("/get/{key}")
async def get_key_value(key: str):
    """从Redis获取指定键的值"""
    async with get_redis() as redis_conn:
        try:
            value = await redis_conn.get(key)
            if value is None:
                return {"message": f"Key '{key}' not found"}
            return {"key": key, "value": value}
        except Exception as e:
            return {"error": f"Failed to get key: {str(e)}"}

@router.delete("/delete/{key}")
async def delete_key(key: str):
    """从Redis删除指定键"""
    async with get_redis() as redis_conn:
        try:
            result = await redis_conn.delete(key)
            if result:
                return {"message": f"Successfully deleted key '{key}'"}
            else:
                return {"message": f"Key '{key}' not found"}
        except Exception as e:
            return {"error": f"Failed to delete key: {str(e)}"}

# 大坑：keys 命令在生产环境中慎用，因为它会阻塞 Redis 服务器
@router.get("/keys")
async def list_keys(pattern: str = "*"):
    """列出匹配模式的所有键"""
    async with get_redis() as redis_conn:
        try:
            keys = await redis_conn.keys(pattern)
            return {"keys": keys}
        except Exception as e:
            return {"error": f"Failed to list keys: {str(e)}"}