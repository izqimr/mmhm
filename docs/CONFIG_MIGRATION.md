# 配置系统迁移记录

## 变更摘要

将所有配置管理从 `config/config.yml` （现已删除）迁移到环境变量系统（`.env` 文件），实现了以下目标：

- ✅ 单一配置源：所有敏感信息和环境相关配置统一在 `.env` 文件中
- ✅ 简化维护：无需维护多份 YAML 配置文件
- ✅ 增强安全性：敏感凭证集中管理，更易于忽略和保护
- ✅ 支持多环境：通过 `ENVIRONMENT` 环境变量轻松切换环境

---

## 影响的类和方法

### 1. `common/yml.py` - 完全重写

**变更前**：
- 从 `config/config.yml` 读取 YAML 配置
- 根据 `API_ENV` 环境变量选择环境配置

**变更后**：
- 直接从 `config.env` 导入预定义的环境变量
- 保持相同的代接口口，确保兼容性

**公开方法**（保持不变）：
```python
yml.get_host()                  # → HOST
yml.get_username()              # → USERNAME
yml.get_password()              # → PASSWORD
yml.get_franchiseDB_info()       # → { DB_host, DB_user, DB_password, DB_port, DataBase }
yml.get_storeDB_info()           # → { DB_host, DB_user, DB_password, DB_port, DataBase }
yml.get_headers()                # → { Content-Type, x-app-id, X-App-Secret }
yml.read_yaml(file_path)         # 读取测试数据文件（不变）
```

### 2. 受影响的模块（无需修改代码，自动适配）

| 模块 | 方法 | 说明 |
|------|------|------|
| **common/auth.py** | `yml.get_password()` | 获取用户密码 |
| | `yml.get_username()` | 获取用户名 |
| **common/request.py** | `yml.get_host()` | 获取 API 主机地址 |
| **common/db.py** | `yml.get_franchiseDB_info()` | 获取数据库配置 |
| | `yml.get_storeDB_info()` | 获取数据库配置 |
| **api/franchise_api.py** | `yml.get_headers()` | 获取请求头 |
| **api/support_api.py** | `yml.get_headers()` | 获取请求头 |

---

## 配置加载链

```
程序启动
    ↓
config/env.py
    ├─ 检查 ENVIRONMENT 环境变量
    ├─ 加载 .env.{ENVIRONMENT} 文件
    ├─ 如不存在，加载 .env 文件
    └─ 读取所有配置变量
    ↓
common/yml.py
    ├─ 从 config.env 导入配置
    ├─ 提供统一的 getter 方法
    └─ 返回配置给调用者
    ↓
业务模块（auth、request、db 等）
    └─ 通过 yml 对象获取需要的配置
```

---

## 环境变量列表

所有配置项必须在 `.env` 文件中定义（参考 `.env.example`）：

### 基本配置
- `ENV` - 环境标识（test|pre|prod）
- `HOST` - API 主机地址
- `USERNAME` - 用户名
- `PASSWORD` - 用户密码
- `APP_ID` - 应用 ID
- `APP_SECRET` - 应用密钥

### Franchise 数据库
- `FRANCHISE_DB_HOST` - 主机地址
- `FRANCHISE_DB_USER` - 用户名
- `FRANCHISE_DB_PASSWORD` - 密码
- `FRANCHISE_DB_PORT` - 端口（默认 3306）
- `FRANCHISE_DATABASE` - 数据库名

### Store 数据库
- `STORE_DB_HOST` - 主机地址
- `STORE_DB_USER` - 用户名
- `STORE_DB_PASSWORD` - 密码
- `STORE_DB_PORT` - 端口（默认 3306）
- `STORE_DATABASE` - 数据库名

### 日志配置
- `LOG_FILE_NAME` - 日志文件名（默认 framework.log）
- `LOG_LEVEL` - 日志级别（DEBUG|INFO|WARNING|ERROR|CRITICAL）

---

## 迁移检查清单

- ✅ `common/yml.py` 已重写，从环境变量读取配置
- ✅ `.env.example` 包含所有必需的配置项
- ✅ `.env.test`、`.env.pre`、`.env.prod` 已创建
- ✅ `config/env.py` 支持环境变量加载
- ✅ `config/config.yml` 已清空（仅含注释）
- ✅ 所有使用 Yml 的模块无需修改（自动适配）
- ✅ `.gitignore` 包含所有 `.env*` 文件

---

## 回滚方法

如果需要回到使用 `config.yml` 的方式，只需：

1. 恢复 `config.yml` 的原始内容（包含所有环境配置）
2. 恢复 `common/yml.py` 的原始实现（解析 YAML）
3. 更新使用 Yml 的所有代码

不过这通常不需要做，新的环境变量方式更简洁、更安全。

---

## 常见问题

### Q: 如何验证配置是否正确加载？

```bash
# 使用编程方式验证
python -c "from common.yml import Yml; yml = Yml(); print(f'Host: {yml.get_host()}')"

# 或查看日志
cat logs/framework.log | grep "logger initialized"
```

### Q: 如果 .env 文件不存在会怎样？

配置系统会使用默认值或抛出 KeyError。确保：
- 至少存在 `.env.test` 或 `.env` 文件
- 所有必需的配置项都有值

### Q: 可以在运行时动态改变配置吗？

可以通过修改 `os.environ`，但由于 Yml 使用单例模式，需要小心处理。建议在程序启动前通过环境变量设置所有配置。

### Q: 多个进程如何使用不同的环境？

在各个进程/线程中启动前设置 `ENVIRONMENT` 环境变量：

```python
import os
os.environ['ENVIRONMENT'] = 'pre'
# 之后启动的代码会使用 pre 环境配置
```

---

## 参考文档

- [README.md](../README.md) - 项目主文档
- [docs/MULTI_ENV_GUIDE.md](../docs/MULTI_ENV_GUIDE.md) - 多环境配置指南
- [config/env.py](../config/env.py) - 环境变量加载逻辑
- [.env.example](../.env.example) - 配置模板
