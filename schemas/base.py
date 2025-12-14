from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

# 泛型类型变量
T = TypeVar('T')


# 通用返回值格式类
class APIRes(BaseModel, Generic[T]):
    """
    通用API返回值格式
    
    Attributes:
        code: 错误码，200表示成功，非200表示失败
        message: 响应消息
        data: 响应数据，可选
    """
    code: int = 200
    message: str = "Success"
    data: Optional[T] = None


# 分页请求基类
class PageParams(BaseModel):
    """
    分页请求参数基类
    
    Attributes:
        page: 页码，从1开始
        page_size: 每页大小
    """
    page: int = 1
    page_size: int = 10


# 分页元数据类
class PageMeta(BaseModel):
    """
    分页元数据
    
    Attributes:
        page: 当前页码
        page_size: 每页大小
        total: 总记录数
        pages: 总页数
    """
    page: int
    page_size: int
    total: int


# 分页响应基类
class PageRes(BaseModel, Generic[T]):
    """
    分页响应数据基类
    
    Attributes:
        items: 数据列表
        meta: 分页元数据
    """
    items: list[T]
    meta: PageMeta
