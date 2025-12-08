from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, func

from core.database import get_db
from models.hero import Hero
from schemas.hero_schemas import HeroCreate, HeroUpdate, Hero as HeroVO, HeroList

router = APIRouter(
    prefix="/heroes",
    tags=["heroes"],
    responses={404: {"description": "Hero not found"}},
)


@router.get("/", response_model=HeroList)
async def read_heroes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """获取英雄列表"""
    # 计算总数
    async with get_db() as db:
        total_result = await db.execute(select(func.count(Hero.id)))
        total = total_result.scalar_one()

        # 获取分页数据
        result = await db.execute(select(Hero).offset(skip).limit(limit))
        heroes = result.scalars().all()

        return HeroList(total=total, items=heroes)


@router.get("/{hero_id}", response_model=HeroVO)
async def read_hero(hero_id: int):
    """获取单个英雄详情"""
    async with get_db() as db:
        result = await db.execute(select(Hero).where(Hero.id == hero_id))
        hero = result.scalar_one_or_none()

        if hero is None:
            raise HTTPException(status_code=404, detail="Hero not found")

        return hero


@router.post("/", response_model=HeroVO, status_code=201)
async def create_hero(hero: HeroCreate):
    """创建新英雄"""
    async with get_db() as db:
        # 检查是否存在同名英雄
        existing_hero = await db.execute(select(Hero).where(Hero.name == hero.name))
        if existing_hero.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Hero with this name already exists")

        db_hero = Hero(**hero.model_dump())
        db.add(db_hero)
        await db.flush()
        await db.refresh(db_hero)

        return db_hero


@router.put("/{hero_id}", response_model=HeroVO)
async def update_hero(
    hero_id: int,
    hero_update: HeroUpdate
):
    """更新英雄信息"""
    async with get_db() as db:
        result = await db.execute(select(Hero).where(Hero.id == hero_id))
        db_hero = result.scalar_one_or_none()

        if db_hero is None:
            raise HTTPException(status_code=404, detail="Hero not found")

        # 检查名称是否重复（如果更新了名称）
        if hero_update.name and hero_update.name != db_hero.name:
            existing_hero = await db.execute(select(Hero).where(Hero.name == hero_update.name))
            if existing_hero.scalar_one_or_none():
                raise HTTPException(status_code=400, detail="Hero with this name already exists")

        # 更新字段
        update_data = hero_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_hero, field, value)

        await db.flush()
        await db.refresh(db_hero)

        return db_hero


@router.delete("/{hero_id}", status_code=204)
async def delete_hero(hero_id: int):
    async with get_db() as db:
        """删除英雄"""
        result = await db.execute(select(Hero).where(Hero.id == hero_id))
        db_hero = result.scalar_one_or_none()

        if db_hero is None:
            raise HTTPException(status_code=404, detail="Hero not found")

        await db.delete(db_hero)
        await db.flush()

        return None