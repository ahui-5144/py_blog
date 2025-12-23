from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class ArticleBase(BaseModel):
    title: str
    content: str


class ArticleCreate(ArticleBase):
    pass  # 只需 title 和 content


class ArticleUpdate(ArticleBase):
    id: int
    author_id: int


class ArticleVO(ArticleBase): # 详情页使用（完整内容）
    id: int
    author_id: int
    create_time: datetime

    class Config:
        from_attributes = True  # 允许从 ORM 模型转换


class ListArticleVO(BaseModel):  # 新增：列表专用模型
    id: int
    title: str
    author_id: int
    summary: str # 内容前20字
    create_time: datetime
    update_time: datetime | None = None

    model_config = ConfigDict(from_attributes=True)