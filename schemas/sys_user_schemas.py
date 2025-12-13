from pydantic import BaseModel


# Token 模型
class Token(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    username: str
    email: str
    nickname: str | None = None
    email: str | None = None
    phone: str | None = None
    avatar: str | None = None
    intro: str | None = None
    role_id: int | None = None


class UserCreate(UserBase):
    password: str
    status: bool = True


class UserUpdate(UserBase):
    password: str | None = None
    status: bool = True


class UserVo(UserBase):
    pass


class UserInDB(UserBase):
    id: int
    status: bool
    deleted: bool
    create_time: str | None = None
    update_time: str | None = None

    # 从数据库模型中读取数据时，将属性映射到模型的属性
    class Config:
        from_attributes = True


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

    class Config:
        from_attributes = True
