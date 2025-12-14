# FastAPI Blog API

一个基于 FastAPI 构建的现代化博客 API 项目，采用分层架构设计，支持异步编程、JWT 认证、Redis 缓存等功能。

## 技术栈

- **框架**: FastAPI 0.100+
- **语言**: Python 3.14
- **ORM**: SQLAlchemy 2.x
- **数据库**: MySQL (异步驱动: asyncmy)
- **缓存**: Redis
- **认证**: JWT + OAuth2
- **文档**: Swagger UI + ReDoc
- **配置管理**: 环境变量 + 集中配置

## 项目特点

- 🔄 **异步编程**: 全面支持异步数据库操作和 Redis 操作
- 🏗️ **分层架构**: 清晰的分层设计，便于维护和扩展
- 🔒 **安全认证**: 基于 JWT 的认证机制，密码加密存储
- 📊 **数据库管理**: 自动创建数据库表，支持数据库连接池配置
- 📝 **自动文档**: 集成 Swagger UI 和 ReDoc，自动生成 API 文档
- 🔧 **配置灵活**: 支持环境变量配置，便于不同环境部署
- 📦 **依赖管理**: 使用 Poetry 进行依赖管理
- 🧪 **测试支持**: 支持单元测试和集成测试

## 项目结构

```
py_blog/
├── api/                   # API 路由层
│   ├── __init__.py
│   └── v1/                # API 版本 1
│       ├── __init__.py
│       ├── router.py      # 路由注册
│       └── endpoints/     # 具体 API 端点
│           ├── __init__.py
│           ├── redis_example.py
│           └── sys_user.py
├── core/                  # 核心配置和基础设施
│   ├── __init__.py
│   ├── config.py          # 配置管理
│   ├── cors.py            # CORS 配置
│   ├── database.py        # 数据库连接
│   ├── dependencies.py    # 依赖注入
│   ├── logger.py          # 日志配置
│   └── redis.py           # Redis 连接
├── dao/                   # 数据访问层
│   ├── __init__.py
│   └── sys_user_dao.py
├── models/                # 数据库模型层
│   ├── __init__.py
│   └── sys_user.py
├── schemas/               # 数据验证层
│   ├── __init__.py
│   ├── base.py
│   └── sys_user_schemas.py
├── services/              # 业务逻辑层
│   ├── __init__.py
│   └── sys_user_service.py
├── utils/                 # 工具函数层
│   ├── __init__.py
│   └── auth.py            # 认证相关工具
├── tests/                 # 测试目录
│   └── __init__.py
├── main.py                # 应用入口
├── requirements.txt       # 依赖列表
├── test_main.http         # HTTP 测试文件
└── README.md              # 项目说明文档
```

## 安装和配置

### 1. 克隆仓库

```bash
git clone https://gitee.com/conspicuous-c/py_blog.git
cd py_blog
```

### 2. 安装依赖

```bash
# 使用 pip
pip install -r requirements.txt

# 或使用 Poetry
poetry install
```

### 3. 配置环境变量

创建 `.env` 文件，配置必要的环境变量：

```env
# 应用基本配置
APP_NAME=FastAPI Blog
DEBUG=True

# 数据库配置
DB_HOST=127.0.0.1
DB_PORT=你的MySQL端口号
DB_USER=你的MySQL用户名
DB_PASSWORD=你的MySQL密码
DB_NAME=fastapi_test

# Redis 配置
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# JWT 配置
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 快速开始

### 1. 运行应用

```bash
# 直接运行
python main.py

# 或使用 uvicorn
uvicorn main:app --host 127.0.0.1 --port 28000 --reload
```

### 2. 访问 API 文档

应用启动后，可以通过以下地址访问 API 文档：

- Swagger UI: http://127.0.0.1:28000/docs
- ReDoc: http://127.0.0.1:28000/redoc

### 3. 测试 API

可以使用 `test_main.http` 文件在 VS Code 中测试 API，或使用其他 HTTP 客户端工具（如 Postman）。

## API 端点

### 用户相关

- `POST /users/token` - 获取访问令牌
- `GET /users/me/` - 获取当前用户信息
- `GET /users/me/items/` - 获取当前用户的物品

### Redis 示例

- `GET /redis/` - Redis 示例接口

## 开发指南

### 1. 添加新的 API 端点

1. 在 `api/v1/endpoints/` 目录下创建新的路由文件
2. 在 `api/v1/router.py` 中注册新路由
3. 在 `main.py` 中 include 新路由

### 2. 添加新的数据库模型

1. 在 `models/` 目录下创建新的模型文件
2. 在 `schemas/` 目录下创建对应的 Pydantic 模型
3. 在 `dao/` 目录下创建数据访问层
4. 在 `services/` 目录下创建业务逻辑层

### 3. 运行测试

```bash
# 运行所有测试
python -m pytest

# 运行特定测试
python -m pytest tests/test_user.py -v
```

### 代码风格

- 遵循 PEP 8 代码风格
- 使用 Black 进行代码格式化
- 使用 MyPy 进行类型检查

## 联系方式

- 项目维护者: [conspicuous-c]

## 更新日志

### v1.0.0 (2025-12-14)

- 初始化项目
- 实现用户认证功能
- 实现 Redis 集成
- 实现基础 API 端点

## 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的 Python Web 框架
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL 工具包和 ORM
- [Redis](https://redis.io/) - 开源内存数据结构存储
- [JWT](https://jwt.io/) - JSON Web 令牌
