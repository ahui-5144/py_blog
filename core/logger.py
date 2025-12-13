import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional

from .config import config

# 创建日志记录器
logger = logging.getLogger("app_logger")
logger.setLevel(getattr(logging, config.LOG_LEVEL.upper(), logging.INFO))

# 定义日志格式
formatter = logging.Formatter(config.LOG_FORMAT)

# 清除现有的处理器，避免重复添加
logger.handlers.clear()

# 添加控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 添加文件处理器（如果配置了日志文件）
if config.LOG_FILE:
    # 确保日志目录存在
    log_dir = os.path.dirname(config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 创建旋转文件处理器
    file_handler = RotatingFileHandler(
        config.LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,  # 保留5个备份文件
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

# 导出日志记录器
app_logger = logger

# 日志装饰器，用于记录函数调用
def log_function(func):
    """
    日志装饰器，用于记录函数调用和返回值
    """
    def wrapper(*args, **kwargs):
        logger.debug(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} returned: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            raise
    return wrapper

# 用于记录HTTP请求的日志函数
def log_http_request(method: str, path: str, status_code: int, duration: float, client_ip: Optional[str] = None):
    """
    记录HTTP请求日志
    
    Args:
        method: HTTP方法
        path: 请求路径
        status_code: HTTP状态码
        duration: 请求处理时间（秒）
        client_ip: 客户端IP地址
    """
    logger.info(
        f"HTTP {method} {path} {status_code} - {duration:.3f}s - {client_ip or 'unknown'}"
    )
