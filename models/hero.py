from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from core.database import Base


class Hero(Base):
    __tablename__ = "hero"

    # id = Column(Integer, primary_key=True, index=True, autoincrement=True)  1.0写法
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True, comment="英雄id")
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True, comment="英雄姓名")
    age: Mapped[int] = mapped_column(Integer, nullable=True, index=True, comment="英雄年龄")
    secret_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="英雄别名")
