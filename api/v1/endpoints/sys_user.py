from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from schemas.base import APIRes
from schemas.sys_user_schemas import Token, User, UserCreate
from services.sys_user_service import SysUserService, get_current_active_user
from utils.auth import create_access_token
from core.config import config

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
    responses={404: {"description": "User not found"}},
)


@router.post("/login")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    获取访问令牌
    
    Args:
        form_data: OAuth2密码请求表单，包含用户名和密码
        db: 数据库会话
    
    Returns:
        Token: 包含访问令牌和令牌类型的响应
    """

    # 认证用户
    user = await SysUserService.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 生成访问令牌
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token":access_token, "token_type": "bearer"}

@router.get("/", response_model=APIRes[User])
async def read_users_me(
        current_user: User = Depends(get_current_active_user)
):
    """
    获取当前用户信息
    
    Args:
        current_user: 当前活动用户orm对象
    
    Returns:
        APIRes[User]: 包含当前用户信息的响应
    """
    return APIRes(data=current_user, message="User information retrieved successfully")


@router.post("/register", response_model=APIRes[User])
async def register_user(user: UserCreate):
    """
    注册新用户

    Args:
        user: 用户注册信息

    Returns:
        APIRes[User]: 包含注册用户信息的响应
    """

    # 检查用户名是否已存在
    existing_user = await SysUserService.get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # 创建新用户
    new_user = await SysUserService.create_user(user)
    return APIRes(data=new_user, message="User registered successfully")
