from datetime import datetime
from typing import List

from sqlalchemy import select, update

from core.database import get_db
from models.article import Article
from schemas.article_schemas import ArticleVO, ArticleUpdate


async def get_all_articles() -> List[ArticleVO]:
    async with (get_db() as db):
        result = await db.execute(select(Article).where(Article.deleted == False))
        return result.scalars().all()


async def get_article_by_id(article_id) -> ArticleVO:
    async with (get_db() as db):
        result = await db.execute(select(Article).where(Article.id == article_id, Article.deleted == False))
        return result.scalars().first()


async def edit_article(article_id: int, article : ArticleUpdate) -> bool:
    async with (get_db() as db):
        # 构建更新数据字典
        update_values = {
            "title": article.title,
            "content": article.content,
            "update_time": datetime.now()
        }

        # 执行更新
        await db.execute(
            update(Article)
            .where(Article.id == article_id, Article.deleted == False)
            .values(update_values)
        )

        # 提交事务
        await db.commit()

        return True
