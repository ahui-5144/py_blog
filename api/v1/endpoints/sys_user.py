from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from core.config import config
from schemas.base import APIRes
from schemas.sys_user_schemas import Token, UserVo, UserCreate
from services.sys_user_service import authenticate_user, get_current_active_user, create_user, get_user_by_username
from utils.auth import create_access_token

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
    responses={404: {"description": "User not found"}},
)

@router.post("/token")
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
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 生成访问令牌
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token":access_token, "token_type": "bearer"}

@router.get("/", response_model=APIRes[UserVo])
async def read_users_me(
        current_user: UserVo = Depends(get_current_active_user)
):
    """
    获取当前用户信息

    Args:
        current_user: 当前活动用户orm对象
    
    Returns:
        APIRes[UserVo]: 包含当前用户信息的响应
    """
    return APIRes(data=current_user, message="User information retrieved successfully")


@router.post("/register", response_model=APIRes[bool])
async def register_user(user: UserCreate):
    """
    注册新用户

    Args:
        user: 用户注册信息

    Returns:
        bool: 注册成功返回True，否则返回False
    """

    # 检查用户名是否已存在
    existing_user = await get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # 创建新用户
    res = await create_user(user) is not None
    return APIRes(data=res, message="User registered successfully")
