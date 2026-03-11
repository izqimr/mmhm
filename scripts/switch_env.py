#!/usr/bin/env python3
"""
环境切换脚本 - 用于快速切换测试环境
"""
import os
import sys
from pathlib import Path

# 确保 PROJECT_ROOT 指向正确的目录
if __name__ == "__main__":
    # 从脚本所在目录开始回溯到项目根目录
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
else:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

def switch_environment(env):
    """
    切换环境
    :param env: test | pre | prod
    """
    env = env.lower()
    
    if env not in ['test', 'pre', 'prod']:
        print(f"❌ 无效的环境: {env}")
        print("✅ 支持的环境: test | pre | prod")
        sys.exit(1)
    
    # 检查环境文件是否存在
    env_file = PROJECT_ROOT / f".env.{env}"
    if not env_file.exists():
        print(f"❌ 环境文件不存在: {env_file}")
        sys.exit(1)
    
    # 设置环境变量（会在本次会话生效）
    os.environ['ENVIRONMENT'] = env
    print(f"\n✅ 已切换到环境: {env}")
    print(f"📝 配置文件: {env_file}")
    
    # 读取并显示配置信息
    with open(env_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('HOST=') or line.startswith('FRANCHISE_DB_HOST='):
                print(f"   {line.strip()}")


def list_environments():
    """列出所有可用环境"""
    print("\n📋 可用的环境配置:\n")
    
    for env in ['test', 'pre', 'prod']:
        env_file = PROJECT_ROOT / f".env.{env}"
        if env_file.exists():
            print(f"  ✅ {env:10s} - {env_file.relative_to(PROJECT_ROOT)}")
        else:
            print(f"  ❌ {env:10s} - 配置文件不存在")
    
    print("\n💡 使用方式:")
    print("  python scripts/switch_env.py test   # 切换到测试环境")
    print("  python scripts/switch_env.py pre    # 切换到预生产环境")
    print("  python scripts/switch_env.py prod   # 切换到生产环境")
    print("\n或设置环境变量:")
    print("  $env:ENVIRONMENT='pre'              # PowerShell")
    print("  export ENVIRONMENT=pre              # Bash/Linux\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        list_environments()
    else:
        env_name = sys.argv[1]
        switch_environment(env_name)
        print()
