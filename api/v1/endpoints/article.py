from typing import List

from fastapi import APIRouter, Depends

from schemas.article_schemas import ArticleVO, ListArticleVO, ArticleUpdate
from schemas.base import APIRes
from schemas.sys_user_schemas import UserVo
from services import article_service
from services.sys_user_service import get_current_active_user

router = APIRouter(
    prefix="/api/v1/article",
    tags=["article"],
    responses={404: {"description": "article not found"}},
)

'''
无需登录就可以查看所有的文章的标题、作者、创建时间、修改时间、内容只展示20个字
'''
@router.get("/",
            summary="获取文章列表（公开，无需登录）",
            response_model=APIRes[List[ListArticleVO]])
async def get_articles():
    articles = await article_service.get_article_list()
    return APIRes(data=articles)

'''
修改文章，只有作者才能修改自己的文章，修改时同时更新修改时间
 current_user: UserVo = Depends(get_current_active_user) 表示从token里面获取用户信息
 
 Depends 本质上就是：在调用你的接口方法之前，先执行另一个函数，把返回值塞进参数里
'''
@router.post("/edit/{article_id}", response_model=APIRes[bool])
async def edit_article(article_id: int,
                       article: ArticleUpdate,
                       current_user: UserVo = Depends(get_current_active_user)):
    res = await article_service.edit_article(article_id, article, current_user)
    return APIRes(data=res, message="edit article successfully")
