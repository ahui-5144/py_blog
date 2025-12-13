from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import config

def setup_cors(app: FastAPI) -> None:
    """
    配置FastAPI应用的CORS中间件
    
    Args:
        app: FastAPI应用实例
    """
    # 配置CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_credentials=config.CORS_CREDENTIALS,
        allow_methods=config.CORS_METHODS,
        allow_headers=config.CORS_HEADERS,
    )
