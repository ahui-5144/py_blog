from typing import List

from fastapi import HTTPException, status

from dao import article_dao
from schemas.article_schemas import ListArticleVO, ArticleVO


async def get_all_articles() -> List[ArticleVO]:
    return await article_dao.get_all_articles()


def to_list_vo(articles) -> List[ListArticleVO]:
    return [
        ListArticleVO(
            id=a.id,
            title=a.title,
            author_id=a.author_id,
            summary=a.content[:20] + ("..." if len(a.content) > 20 else ""),
            create_time=a.create_time,
            update_time=a.update_time,
        )
        for a in articles
    ]


async def get_article_list() -> List[ListArticleVO]:
    articles = await get_all_articles()
    return to_list_vo(articles)


'''
修改文章，只能修改自己的文章
'''


async def edit_article(article_id, article, current_user) -> bool:
    article_target = await article_dao.get_article_by_id(article_id)
    if not article_target:
        # 报错 提示文章不存在
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )

    if article_target.author_id != current_user.id:
        # 报错提示只能修改自己的文章
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改他人的文章"
        )
    return await article_dao.edit_article(article_id, article)