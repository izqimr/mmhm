# 多环境配置指南

## 概述

该框架支持三个环境配置：
- **test** - 测试环境
- **pre** - 预生产环境
- **prod** - 生产环境

每个环境有独立的配置文件，包括不同的主机地址、数据库连接、用户凭证等。

---

## 文件结构

```
.env                # 本地开发配置（.gitignore 中，不提交）
.env.example        # 模板文件（提交到 Git，供参考）
.env.test           # 测试环境配置（.gitignore 中，不提交）
.env.pre            # 预生产环境配置（.gitignore 中，不提交）
.env.prod           # 生产环境配置（.gitignore 中，不提交）

scripts/
  └── switch_env.py # 环境切换辅助脚本
```

---

## 环境变量加载优先级

config/env.py 按以下优先级加载配置：

```
1. OS 环境变量 ENVIRONMENT  (最高优先级)
   ↓
2. .env.{ENVIRONMENT} 文件  (如 .env.test)
   ↓
3. .env 文件              (本地开发，不存在时跳过)
   ↓
4. 默认值 'test'          (最低优先级)
```

---

## 使用方式

### 方式 1：环境变量（推荐用于 CI/CD）

#### PowerShell
```powershell
# 切换到测试环境
$env:ENVIRONMENT='test'
pytest

# 切换到预生产环境
$env:ENVIRONMENT='pre'
pytest

# 切换到生产环境
$env:ENVIRONMENT='prod'
pytest
```

#### Bash/Linux/Mac
```bash
# 切换到测试环境
export ENVIRONMENT=test
pytest

# 切换到预生产环境
export ENVIRONMENT=pre
pytest

# 切换到生产环境
export ENVIRONMENT=prod
pytest
```

### 方式 2：脚本切换（推荐用于本地开发）

```bash
# 查看所有可用环境
python scripts/switch_env.py

# 切换到测试环境
python scripts/switch_env.py test

# 切换到预生产环境
python scripts/switch_env.py pre

# 切换到生产环境
python scripts/switch_env.py prod
```

### 方式 3：默认行为

不设置 `ENVIRONMENT` 环境变量时，框架默认加载 `.env.test` 配置。

---

## 配置文件内容说明

每个环境配置文件包含以下部分：

```env
# 1. 环境标识
ENV=test

# 2. 公共配置（API 相关）
HOST=https://test-digital.hnlshm.com
USERNAME=your_username
PASSWORD=your_password
APP_ID=store-selection-service
APP_SECRET=your_app_secret

# 3. Franchise 数据库配置
FRANCHISE_DB_HOST=mysql.example.com
FRANCHISE_DB_USER=store_franchise_user
FRANCHISE_DB_PASSWORD=your_password
FRANCHISE_DB_PORT=3306
FRANCHISE_DATABASE=store_franchise

# 4. Store 数据库配置
STORE_DB_HOST=mysql.example.com
STORE_DB_USER=store_core_user
STORE_DB_PASSWORD=your_password
STORE_DB_PORT=3306
STORE_DATABASE=store_core

# 5. 日志配置
LOG_FILE_NAME=framework.log
LOG_LEVEL=INFO
```

---

## 初始化步骤

### 1. 复制模板文件

```bash
cp .env.example .env.test
cp .env.example .env.pre
cp .env.example .env.prod
```

### 2. 编辑配置文件

编辑每个环境的配置文件，替换占位符为实际的值：

```bash
# 编辑测试环境配置
vim .env.test

# 编辑预生产环境配置
vim .env.pre

# 编辑生产环境配置
vim .env.prod
```

### 3. 验证配置

```bash
# 验证测试环境
$env:ENVIRONMENT='test'
python -c "from config.env import HOST, FRANCHISE_DB_HOST; print(f'Host: {HOST}'); print(f'DB: {FRANCHISE_DB_HOST}')"

# 验证预生产环境
$env:ENVIRONMENT='pre'
python -c "from config.env import HOST, FRANCHISE_DB_HOST; print(f'Host: {HOST}'); print(f'DB: {FRANCHISE_DB_HOST}')"
```

---

## CI/CD 集成

### GitHub Actions 示例

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [test, pre]
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        env:
          ENVIRONMENT: ${{ matrix.environment }}
        run: pytest -v
```

### GitHub Secrets 管理

在 GitHub Actions 中，敏感信息应通过 Secrets 传入：

```yaml
- name: Create .env file
  env:
    ENVIRONMENT: test
    HOST: ${{ secrets.TEST_HOST }}
    USERNAME: ${{ secrets.TEST_USERNAME }}
    PASSWORD: ${{ secrets.TEST_PASSWORD }}
  run: |
    cat > .env.test << EOF
    ENV=test
    HOST=${{ env.HOST }}
    USERNAME=${{ env.USERNAME }}
    PASSWORD=${{ env.PASSWORD }}
    ...
    EOF
```

---

## 安全最佳实践

### ✅ 推荐做法

1. **本地开发**
   - 使用 `.env.local` 或 `.env` 存储本地凭证
   - 永不提交到 Git

2. **CI/CD 环境**
   - 使用平台的 Secrets 管理工具（GitHub Secrets、GitLab Variables 等）
   - 不在代码中硬编码凭证

3. **生产环境**
   - 使用环境变量或密钥管理服务（如 AWS Secrets Manager）
   - 限制凭证的访问权限

### ❌ 避免做法

- ❌ 提交 `.env` 或 `.env.*` 文件到 Git
- ❌ 在代码中硬编码密码
- ❌ 使用过期的凭证
- ❌ 在多个环境间共享凭证

---

## 常见问题

### Q: 如何知道当前使用的是哪个环境？

```bash
python -c "from config.env import APP_ENV; print(f'Current env: {APP_ENV}')"
```

### Q: 如何在运行测试时动态切换环境？

```bash
$env:ENVIRONMENT='pre'; pytest testcase/franchise/ -v
```

### Q: .env.example 需要提交到 Git 吗？

是的，`.env.example` 是模板文件，应提交到 Git，以便新团队成员参考。

### Q: 能否为不同的测试套件使用不同的环境？

可以：

```bash
# 针对测试环境的测试
$env:ENVIRONMENT='test'; pytest testcase/api/ -v

# 针对生产环境的冒烟测试
$env:ENVIRONMENT='prod'; pytest testcase/smoke/ -v
```

---

## 相关文件

- [README.md](../README.md) - 项目主文档
- [config/env.py](../config/env.py) - 环境配置加载逻辑
- [.env.example](../.env.example) - 配置模板
- [scripts/switch_env.py](../scripts/switch_env.py) - 环境切换脚本
