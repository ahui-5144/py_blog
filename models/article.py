from datetime import datetime

from sqlalchemy import Column, BigInteger, String, Text, DateTime, text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base

'''
这里的base是什么意思？ 有什么作用？

继承 Base 的类实例可作为 ORM 对象使用，支持：
查询：session.query(Article).filter_by(...)
添加/更新/删除：session.add(article_instance)
关系加载：通过 relationship 定义的外键关联。
'''
class Article(Base):
    __tablename__ = 'article'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, comment="文章id")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="文章标题")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="文章内容")

    # 作者外键：引用 SysUser 表的 id
    author_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("sys_user.id", ondelete="SET NULL"),  # 假设 SysUser 表名为 sys_user，根据实际调整
        nullable=True,  # 或 False，根据需求
        comment="作者id"
    )
    deleted: Mapped[bool] = mapped_column(Boolean, default=False, comment="逻辑删除 0-未删除 1-已删除")
    create_time: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text('CURRENT_TIMESTAMP'),
        comment="创建时间"
    )
    update_time: Mapped[datetime] = mapped_column(DateTime, nullable=True,
                                                  server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
                                                  onupdate=text('CURRENT_TIMESTAMP'), comment="更新时间")