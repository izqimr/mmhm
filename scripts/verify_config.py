#!/usr/bin/env python3
"""验证配置系统是否正常工作"""
import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

try:
    from common.yml import Yml
    
    yml = Yml()
    env = os.getenv('ENVIRONMENT', 'test')
    
    print(f'\n=== 配置验证（环境: {env}）===\n')
    
    # 测试基本配置
    print(f'✓ Host:      {yml.get_host()}')
    print(f'✓ Username:  {yml.get_username()}')
    
    # 测试数据库配置
    db_info = yml.get_franchiseDB_info()
    print(f'✓ Franchise DB Host:  {db_info["DB_host"]}')
    
    # 测试请求头
    headers = yml.get_headers()
    print(f'✓ Headers:   {list(headers.keys())}')
    
    print('\n✅ 所有配置均已正确加载\n')
    
except Exception as e:
    print(f'\n❌ 配置验证失败：{e}\n')
    sys.exit(1)
