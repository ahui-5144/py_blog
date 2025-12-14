from sqlalchemy import select

from core.database import get_db
from models.sys_user import SysUser
from schemas.sys_user_schemas import UserCreate
from utils.auth import verify_password, get_password_hash


class SysUserDao:
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
        async with (get_db() as db):
            result = await db.execute(select(SysUser).where(SysUser.username == username, SysUser.deleted == False))
            return result.scalars().first()

    @staticmethod
    async def get_user_by_user_id(user_id: int) -> SysUser | None:
        """
        根据用户ID获取用户信息

        Args:
            user_id: 用户ID

        Returns:
            SysUser: 用户对象，不存在则返回None
        """
        async with get_db() as db:
            result = await db.execute(select(SysUser).where(SysUser.id == user_id, SysUser.deleted == False))
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
        user = await SysUserDao.get_user_by_username(username)
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
