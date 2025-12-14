from typing import Annotated

from fastapi import Depends, HTTPException, status

from dao.sys_user_dao import SysUserDao
from models.sys_user import SysUser
from schemas.sys_user_schemas import UserVo, UserCreate
from utils.auth import decode_token, oauth2_scheme


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    从JWT中获取当前用户
    
    Args:
        token: JWT令牌
        
    Returns:
        SysUser: 当前用户对象
    """
    user_id = decode_token(token)
    user = await SysUserDao.get_user_by_user_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_active_user(current_user: Annotated[UserVo, Depends(get_current_user)]):
    """
    验证当前用户是否为活动用户
    
    Args:
        current_user: 当前用户orm对象
        
    Returns:
        UserVo: 活动用户对象
    """
    if not current_user.status:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


async def create_user(user: UserCreate) -> SysUser:
    """
    创建新用户

    Args:
        user: 用户创建数据

    Returns:
        SysUser: 创建的用户对象
    """
    return await SysUserDao.create_user(user)


async def authenticate_user(username: str, password: str) -> SysUser | bool:
    """
    认证用户，验证用户名和密码是否正确

    Args:
        username: 用户名
        password: 密码

    Returns:
        SysUser: 认证成功返回用户对象，失败返回False
    """
    return await SysUserDao.authenticate_user(username, password)


async def get_user_by_username(username: str) -> SysUser | None:
    """
    根据用户名获取用户信息

    Args:
        username: 用户名

    Returns:
        SysUser: 用户对象，不存在则返回None
    """
    return await SysUserDao.get_user_by_username(username)
