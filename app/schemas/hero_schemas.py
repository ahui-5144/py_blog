from pydantic import BaseModel, ConfigDict
from typing import Optional


# Hero DTOs (数据传输对象)
class HeroBase(BaseModel):
    name: str
    age: Optional[int] = None
    secret_name: str


class HeroCreate(HeroBase):
    """创建英雄时使用的DTO"""
    pass


class HeroUpdate(HeroBase):
    """更新英雄时使用的DTO，所有字段可选"""
    name: Optional[str] = None
    secret_name: Optional[str] = None


# Hero VOs (视图对象)
class Hero(HeroBase):
    """英雄详情视图对象"""
    model_config = ConfigDict(from_attributes=True)
    id: int


class HeroList(BaseModel):
    """英雄列表视图对象"""
    total: int
    items: list[Hero]