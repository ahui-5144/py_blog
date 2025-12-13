import os
from typing import Any, Dict, Optional

class Config:
    """应用配置类"""
    
    # 应用基本配置
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI Blog")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
    
    # 数据库配置
    DB_HOST: str = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT: int = int(os.getenv("DB_PORT", "33061"))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "200099")
    DB_NAME: str = os.getenv("DB_NAME", "fastapi_test")
    DB_CHARSET: str = os.getenv("DB_CHARSET", "utf8mb4")
    
    # SQLAlchemy配置
    SQLALCHEMY_DATABASE_URL: str = (
        f"mysql+asyncmy://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"
    )
    
    # 数据库连接池配置
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "10"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "20"))
    DB_POOL_TIMEOUT: int = int(os.getenv("DB_POOL_TIMEOUT", "30"))
    DB_POOL_RECYCLE: int = int(os.getenv("DB_POOL_RECYCLE", "3600"))
    DB_POOL_PRE_PING: bool = os.getenv("DB_POOL_PRE_PING", "True").lower() in ("true", "1", "yes")
    
    # Redis配置
    REDIS_HOST: str = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD")
    REDIS_MAX_CONNECTIONS: int = int(os.getenv("REDIS_MAX_CONNECTIONS", "20"))
    
    # 日志配置
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO" if not DEBUG else "DEBUG")
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE")
    LOG_FORMAT: str = os.getenv(
        "LOG_FORMAT",
        "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s"
    )
    
    # CORS配置
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")
    CORS_METHODS: list = os.getenv("CORS_METHODS", "GET,POST,PUT,DELETE,PATCH,OPTIONS").split(",")
    CORS_HEADERS: list = os.getenv("CORS_HEADERS", "*").split(",")
    CORS_CREDENTIALS: bool = os.getenv("CORS_CREDENTIALS", "True").lower() in ("true", "1", "yes")

    # SECURITY配置
    # 密钥 在 Git Bash 使用命令: openssl rand -hex 32 获取
    SECRET_KEY: str = os.getenv("SECRET_KEY", "bf20c50780fe5b505ba68d8ef9dc40ea30bb3fa73514279eaa50119cd8032483")
    # 加密算法
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    # 过期时间
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# 创建配置实例
config = Config()

# 导出配置字典，方便在需要时使用
def get_config_dict() -> Dict[str, Any]:
    """获取配置字典"""
    return {
        "app_name": config.APP_NAME,
        "debug": config.DEBUG,
        "database": {
            "url": config.SQLALCHEMY_DATABASE_URL,
            "pool_size": config.DB_POOL_SIZE,
            "max_overflow": config.DB_MAX_OVERFLOW,
            "pool_timeout": config.DB_POOL_TIMEOUT,
            "pool_recycle": config.DB_POOL_RECYCLE,
            "pool_pre_ping": config.DB_POOL_PRE_PING,
        },
        "redis": {
            "host": config.REDIS_HOST,
            "port": config.REDIS_PORT,
            "db": config.REDIS_DB,
            "password": config.REDIS_PASSWORD,
            "max_connections": config.REDIS_MAX_CONNECTIONS,
        },
        "log": {
            "level": config.LOG_LEVEL,
            "file": config.LOG_FILE,
            "format": config.LOG_FORMAT,
        },
        "cors": {
            "origins": config.CORS_ORIGINS,
            "methods": config.CORS_METHODS,
            "headers": config.CORS_HEADERS,
            "credentials": config.CORS_CREDENTIALS,
        },
        "security": {
            "secret_key": config.SECRET_KEY,
            "algorithm": config.ALGORITHM,
            "access_token_expire_minutes": config.ACCESS_TOKEN_EXPIRE_MINUTES,
        }
    }
