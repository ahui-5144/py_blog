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
    class Config:
        from_attributes = True
