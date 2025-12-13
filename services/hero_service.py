from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.hero import Hero
from schemas.base import PageParams
from schemas.hero_schemas import HeroCreate, HeroUpdate


class HeroService:
    """英雄服务类，处理英雄相关的业务逻辑"""
    
    @staticmethod
    async def get_heroes(db: AsyncSession, pagination: PageParams):
        """
        获取英雄列表
        
        Args:
            db: 数据库会话
            pagination: 分页参数
        
        Returns:
            tuple: (英雄列表, 总记录数)
        """
        # 计算总数
        total_result = await db.execute(select(func.count(Hero.id)))
        total = total_result.scalar_one()

        # 计算偏移量
        offset = (pagination.page - 1) * pagination.page_size

        # 获取分页数据
        result = await db.execute(select(Hero).offset(offset).limit(pagination.page_size))
        heroes = result.scalars().all()

        return heroes, total
    
    @staticmethod
    async def get_hero_by_id(db: AsyncSession, hero_id: int):
        """
        根据ID获取英雄详情
        
        Args:
            db: 数据库会话
            hero_id: 英雄ID
        
        Returns:
            Hero: 英雄对象，不存在则返回None
        """
        result = await db.execute(select(Hero).where(Hero.id == hero_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create_hero(db: AsyncSession, hero_create: HeroCreate):
        """
        创建新英雄
        
        Args:
            db: 数据库会话
            hero_create: 英雄创建数据
        
        Returns:
            Hero: 创建的英雄对象
        
        Raises:
            ValueError: 如果英雄名称已存在
        """
        # 检查是否存在同名英雄
        existing_hero = await db.execute(select(Hero).where(Hero.name == hero_create.name))
        if existing_hero.scalar_one_or_none():
            raise ValueError("Hero with this name already exists")

        db_hero = Hero(**hero_create.model_dump())
        db.add(db_hero)
        await db.flush()
        await db.refresh(db_hero)

        return db_hero
    
    @staticmethod
    async def update_hero(db: AsyncSession, hero_id: int, hero_update: HeroUpdate):
        """
        更新英雄信息
        
        Args:
            db: 数据库会话
            hero_id: 英雄ID
            hero_update: 英雄更新数据
        
        Returns:
            Hero: 更新后的英雄对象，不存在则返回None
        
        Raises:
            ValueError: 如果英雄名称已存在
        """
        # 获取英雄
        result = await db.execute(select(Hero).where(Hero.id == hero_id))
        db_hero = result.scalar_one_or_none()

        if db_hero is None:
            return None

        # 检查名称是否重复（如果更新了名称）
        if hero_update.name and hero_update.name != db_hero.name:
            existing_hero = await db.execute(select(Hero).where(Hero.name == hero_update.name))
            if existing_hero.scalar_one_or_none():
                raise ValueError("Hero with this name already exists")

        # 更新字段
        update_data = hero_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_hero, field, value)

        await db.flush()
        await db.refresh(db_hero)

        return db_hero
    
    @staticmethod
    async def delete_hero(db: AsyncSession, hero_id: int):
        """
        删除英雄
        
        Args:
            db: 数据库会话
            hero_id: 英雄ID
        
        Returns:
            bool: 删除成功返回True，不存在返回False
        """
        # 获取英雄
        result = await db.execute(select(Hero).where(Hero.id == hero_id))
        db_hero = result.scalar_one_or_none()

        if db_hero is None:
            return False

        await db.delete(db_hero)
        await db.flush()

        return True
