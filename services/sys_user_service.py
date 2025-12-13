from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.sys_user import SysUser
from schemas.sys_user_schemas import User, UserInDB, UserCreate
from utils.auth import decode_token, oauth2_scheme, get_password_hash, verify_password


class SysUserService:
    """用户服务类，处理用户相关的业务逻辑"""
    
    @staticmethod
    async def get_user_by_username(username: str) -> SysUser | None:
        """
        根据用户名获取用户信息
        
        Args:
            username: 用户名
        
        Returns:
            SysUser: 用户对象，不存在则返回None
        """
        async with get_db() as db:
            result = await db.execute(select(SysUser).where(SysUser.username == username, SysUser.deleted == False))
            return result.scalars().first()
    
    @staticmethod
    async def authenticate_user(username: str, password: str) -> SysUser | bool:
        """
        认证用户，验证用户名和密码是否正确
        
        Args:
            username: 用户名
            password: 密码
        
        Returns:
            SysUser: 认证成功返回用户对象，失败返回False
        """
        user = await SysUserService.get_user_by_username(username)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user
    
    @staticmethod
    async def create_user(user: UserCreate) -> SysUser:
        """
        创建新用户
        
        Args:
            user: 用户创建数据
        
        Returns:
            SysUser: 创建的用户对象
        """
        async with get_db() as db:
            # 获取用户数据并加密密码
            user_data = user.model_dump()
            plain_password = user_data.pop("password")
            hashed_password = get_password_hash(plain_password)

            # 创建用户对象
            db_user = SysUser(
                password=hashed_password,
                **user_data
            )

            db.add(db_user)
            await db.flush()
            await db.refresh(db_user)
            return db_user


# 获取当前用户
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    从JWT中获取当前用户
    
    Args:
        token: JWT令牌
        db: 数据库会话
        
    Returns:
        UserInDB: 当前用户对象
    """
    username = decode_token(token)
    user = await SysUserService.get_user_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


# 获取当前活动用户
async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    """
    验证当前用户是否为活动用户
    
    Args:
        current_user: 当前用户orm对象
        
    Returns:
        User: 活动用户对象
    """
    if not current_user.status:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return current_user
