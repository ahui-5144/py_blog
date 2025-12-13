from fastapi import APIRouter, HTTPException, Depends

from core.database import get_db
from schemas.base import APIRes, PageParams, PageRes, PageMeta
from schemas.hero_schemas import HeroCreate, HeroUpdate, Hero as HeroVO
from services.hero_service import HeroService

router = APIRouter(
    prefix="/heroes",
    tags=["heroes"],
    responses={404: {"description": "Hero not found"}},
)


@router.get("/", response_model=APIRes[PageRes[HeroVO]])
async def read_heroes(
    pagination: PageParams = Depends()
):
    """获取英雄列表"""
    async with get_db() as db:
        # 调用服务层获取英雄列表
        heroes, total = await HeroService.get_heroes(db, pagination)

        # 构造分页响应
        pagination_data = PageRes(
            items=heroes,
            meta=PageMeta(
                page=pagination.page,
                page_size=pagination.page_size,
                total=total
            )
        )

        return APIRes(data=pagination_data)


@router.get("/{hero_id}", response_model=APIRes[HeroVO])
async def read_hero(hero_id: int):
    """获取单个英雄详情"""
    async with get_db() as db:
        # 调用服务层获取英雄详情
        hero = await HeroService.get_hero_by_id(db, hero_id)

        if hero is None:
            raise HTTPException(status_code=404, detail="Hero not found")

        return APIRes(data=hero)


@router.post("/", response_model=APIRes[HeroVO], status_code=201)
async def create_hero(hero: HeroCreate):
    """创建新英雄"""
    async with get_db() as db:
        try:
            # 调用服务层创建英雄
            db_hero = await HeroService.create_hero(db, hero)
            return APIRes(data=db_hero, message="Hero created successfully")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))


@router.put("/{hero_id}", response_model=APIRes[HeroVO])
async def update_hero(
    hero_id: int,
    hero_update: HeroUpdate
):
    """更新英雄信息"""
    async with get_db() as db:
        try:
            # 调用服务层更新英雄
            db_hero = await HeroService.update_hero(db, hero_id, hero_update)
            
            if db_hero is None:
                raise HTTPException(status_code=404, detail="Hero not found")
            
            return APIRes(data=db_hero, message="Hero updated successfully")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{hero_id}", response_model=APIRes)
async def delete_hero(hero_id: int):
    """删除英雄"""
    async with get_db() as db:
        # 调用服务层删除英雄
        success = await HeroService.delete_hero(db, hero_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Hero not found")
        
        return APIRes(message="Hero deleted successfully")