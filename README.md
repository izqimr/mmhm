# 自动化测试框架

企业级 API 自动化测试框架，基于 Pytest + Python 构建。

## 📋 项目概述

本框架提供了完整的自动化测试解决方案，支持：
- ✅ 多环境配置（test/pre/prod）
- ✅ API 接口自动化测试
- ✅ 数据库验证
- ✅ 详细日志记录
- ✅ 自动重试机制

---

## 🏗️ 项目结构

```
autoTest/
├── api/                    # API 测试层
│   ├── franchise_api.py    # 加盟相关API
│   ├── selection_api.py    # 选店相关API
│   └── support_api.py      # 支持相关API
├── common/                 # 公共模块
│   ├── auth.py            # 认证管理
│   ├── request.py         # HTTP 请求封装
│   ├── db.py              # 数据库操作
│   ├── logger.py          # 日志管理
│   ├── yml.py             # YAML 配置解析
│   ├── assertion.py       # 自定义断言
│   └── ...
├── config/                # 配置目录 (只有 env.py，已不再包含 config.yml)
│   └── env.py             # 环境变量读取
├── data/                  # 测试数据
│   ├── franchise/         # 加盟测试数据
│   ├── selection/         # 选店测试数据
│   └── ...
├── testcase/              # 测试用例
│   ├── franchise/         # 加盟测试用例
│   ├── selection/         # 选店测试用例
│   └── ...
├── logs/                  # 测试日志输出
├── conftest.py            # Pytest 全局配置
├── pytest.ini             # Pytest 配置文件
├── requirements.txt       # Python 依赖
├── scripts/               # 工具脚本
│   └── switch_env.py      # 环境切换脚本
├── .env                   # 环境变量（本地开发，不提交）
├── .env.example           # 环境变量模板（提交到Git）
├── .env.test              # 测试环境配置（不提交）
├── .env.pre               # 预生产环境配置（不提交）
├── .env.prod              # 生产环境配置（不提交）
└── README.md              # 项目文档
```

---

## 🚀 快速开始

### 1. 环境准备

**Python 版本**：3.8+

**安装依赖**：
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

#### 单环境配置（本地开发）

创建 `.env` 文件（基于 `.env.example`）：
```bash
cp .env.example .env
```

编辑 `.env` 文件，填入实际的配置信息：
```env
ENV=test
HOST=https://your-host.com
USERNAME=your_username
PASSWORD=your_password
FRANCHISE_DB_HOST=your_db_host
FRANCHISE_DB_USER=your_db_user
FRANCHISE_DB_PASSWORD=your_db_password
```

#### 多环境配置（推荐）

框架支持多个环境配置文件，优先级从高到低：

```
.env.{ENVIRONMENT}  (由环境变量 ENVIRONMENT 决定)
├── .env.test       # 测试环境配置
├── .env.pre        # 预生产环境配置
└── .env.prod       # 生产环境配置
```

**创建环境配置文件**：
```bash
# 复制模板
cp .env.example .env.test
cp .env.example .env.pre
cp .env.example .env.prod

# 编辑每个环境的配置
# vim .env.test   # 填入测试环境凭证
# vim .env.pre    # 填入预生产环境凭证
# vim .env.prod   # 填入生产环境凭证
```

**切换环境方式**：

方式1：使用环境变量（推荐）
```bash
# PowerShell
$env:ENVIRONMENT='test'
pytest

$env:ENVIRONMENT='pre'
pytest

$env:ENVIRONMENT='prod'
pytest
```

```bash
# Bash/Linux
export ENVIRONMENT=test
pytest

export ENVIRONMENT=pre
pytest

export ENVIRONMENT=prod
pytest
```

方式2：使用切换脚本
```bash
python scripts/switch_env.py test   # 切换到测试环境
python scripts/switch_env.py pre    # 切换到预生产环境
python scripts/switch_env.py prod   # 切换到生产环境
```

**环境配置文件说明**：

| 文件 | 用途 | 日志级别 | 说明 |
|------|------|---------|------|
| `.env` | 本地开发 | DEBUG | 未提交到Git |
| `.env.example` | 配置模板 | INFO | 提交到Git，作为参考 |
| `.env.test` | 测试环境 | INFO | 不提交到Git |
| `.env.pre` | 预生产环境 | INFO | 不提交到Git |
| `.env.prod` | 生产环境 | ERROR | 不提交到Git |

### 3. 运行测试

**运行所有测试**：
```bash
pytest
```

**运行特定测试文件**：
```bash
pytest testcase/franchise/test_create_store.py -v
```

**运行并生成覆盖率报告**：
```bash
pytest --cov=api --cov=common --cov-report=html
```

**并行运行测试**：
```bash
pytest -n auto
```

---

## 📝 常用命令

| 命令 | 说明 |
|------|------|
| `pytest` | 运行所有测试 |
| `pytest -v` | 详细输出 |
| `pytest -k "test_create"` | 运行匹配的测试 |
| `pytest tesecase/franchise/` | 运行特定目录的测试 |
| `pytest --collect-only` | 仅收集测试但不执行 |
| `pytest -x` | 第一个失败时停止 |
| `pytest --lf` | 运行上次失败的测试 |
| `pytest --maxfail=3` | 失败3次后停止 |
| `pytest -n auto` | 并行执行测试 |
| `pytest --alluredir=./allure-results` | 生成 Allure 报告 |

---

## ⚙️ 配置系统

### 配置说明

所有配置已从传统的 `config.yml` 迁移到环境变量系统（`.env` 文件）管理，具有以下优势：

- ✅ **单一配置源** - 所有敏感信息集中管理
- ✅ **安全性更高** - 敏感凭证不提交到 Git
- ✅ **多环境支持** - 轻松切换 test/pre/prod 环境
- ✅ **符合 12-factor app** - 配置与代码分离

**详细信息请查看**：[docs/CONFIG_MIGRATION.md](docs/CONFIG_MIGRATION.md) 与 [docs/MULTI_ENV_GUIDE.md](docs/MULTI_ENV_GUIDE.md)

### 快速查询配置

```python
from common.yml import Yml

yml = Yml()

# 获取基本配置
host = yml.get_host()
username = yml.get_username()
password = yml.get_password()
headers = yml.get_headers()

# 获取数据库配置
franchise_db = yml.get_franchiseDB_info()
store_db = yml.get_storeDB_info()
```

---

## 🔧 框架特性

### 认证管理
```python
from common.auth import Auth

auth = Auth()
token = auth.login()  # 自动获取 token
```

### HTTP 请求
```python
from common.request import Request

request = Request()
response = request.send(
    method="POST",
    url="/api/endpoint",
    json={"key": "value"},
    need_token=True  # 自动添加认证令牌
)
```

### 数据库操作
```python
from common.db import DB

db = DB("franchise")
result = db.execute(
    "SELECT * FROM t_franchise_intention WHERE intention_no = %s",
    ("YX2026030600200008288",)
)
```

### 日志记录
```python
from common.logger import get_logger

logger = get_logger(__name__)
logger.info("测试开始")
logger.error("出错了")
```

### YAML 测试数据
```python
from common.yml import Yml

yml = Yml()
data = yml.read_yaml("data/franchise/create_store.yml")
```

---

## 📊 测试报告

### 日志位置
测试日志输出到 `logs/framework.log`

### 配置日志级别
编辑 `.env`：
```env
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

---

## 🔐 安全说明

⚠️ **敏感信息管理**：
- ✅ 所有敏感信息（密码、凭证、API KEY）存储在 `.env` 文件中
- ✅ `.env` 已添加到 `.gitignore`，不会被提交到 Git
- ✅ 使用 `.env.example` 作为模板，提交到 Git 供他人参考

**永远不要**：
- ❌ 提交 `.env` 文件到 Git
- ❌ 在代码中硬编码敏感信息

---

## 🐛 故障排除

### 问题：导入错误 `ModuleNotFoundError`

**解决方案**：确保已安装依赖
```bash
pip install -r requirements.txt
```

### 问题：数据库连接失败

**解决方案**：检查 `.env` 中的数据库配置是否正确

### 问题：认证失败

**解决方案**：验证 `.env` 中的用户名和密码

---

## 📚 最佳实践

### 1. 测试用例编写
```python
import pytest
from api.franchise_api import FranchiseApi

class TestFranchise:
    """加盟相关测试"""
    
    def test_create_intention(self, logger):
        """测试创建意向"""
        logger.info("开始测试创建意向")
        
        franchise = FranchiseApi()
        response = franchise.create_intention(...)
        
        assert response.get("success") is True
```

### 2. 使用 Fixtures
```python
@pytest.fixture
def test_data():
    """测试数据 fixture"""
    return {"key": "value"}

def test_example(test_data, logger):
    """使用 fixture 的测试"""
    logger.info(f"测试数据: {test_data}")
```

### 3. 参数化测试
```python
@pytest.mark.parametrize("province,city", [
    ("440000", "440400"),
    ("440000", "440500"),
])
def test_create_store(province, city):
    """参数化测试"""
    pass
```

---

## 🤝 贡献指南

1. 创建 feature 分支
2. 提交变更
3. 推送到远程
4. 创建 Pull Request

---

## 📞 联系方式

如有问题或建议，请联系项目维护者。

---

## 📄 许可证

MIT License
