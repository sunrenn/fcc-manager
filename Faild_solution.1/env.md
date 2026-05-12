---
name: env.py
description: 环境配置加载和变量管理
---

## 使用说明

### 环境配置加载

1. **初始化环境**：调用 `load_env()` 加载环境变量
2. **获取变量**：使用 `get_env_var(key, default=None)` 获取环境变量
3. **设置变量**：使用 `set_env_var(key, value)` 设置或覆盖环境变量
4. **批量更新**：使用 `update_from_dict(env_dict)` 批量更新环境变量
5. **获取所有变量**：使用 `get_all_vars()` 获取所有当前环境变量
6. **检查变量**：使用 `has_var(key)` 检查变量是否存在
7. **重置环境**：使用 `reset()` 清空所有环境变量

### 测试驱动开发

测试文件结构：
- `test_env_var()` - 测试环境变量获取
- `test_env_var_default()` - 测试默认值处理
- `test_update_from_dict()` - 测试批量更新
- `test_has_var()` - 测试变量检查
- `test_reset()` - 测试重置功能
- `test_get_all_vars()` - 测试获取所有变量

### 使用示例

```python
from env import env, load_env, get_env_var, set_env_var

# 加载环境
load_env()

# 获取变量
db_host = get_env_var('DB_HOST')

# 设置变量
set_env_var('TEST_MODE', 'true')

# 检查变量
if env.has_var('CUSTOM_VAR'):
    custom = env.get('CUSTOM_VAR')
