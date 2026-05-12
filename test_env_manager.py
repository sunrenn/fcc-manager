# test_env_manager.py
import sys
sys.path.insert(0, '.')

from env_manager import EnvManager


def test_read_env_from_string():
    """测试从字符串读取.env 内容"""
    # 预期的.env 内容
    env_content = """
    API_KEY=sk-123456
    DATABASE_URL=postgresql://localhost/db
    DEBUG=True
    """
    
    # 创建 EnvManager 实例
    manager = EnvManager()
    
    # 期望解析后的字典
    expected = {
        'API_KEY': 'sk-123456',
        'DATABASE_URL': 'postgresql://localhost/db',
        'DEBUG': 'True'
    }
    
    # 断言：测试会失败
    result = manager.read_from_string(env_content)
    assert result == expected, f"Expected {expected}, got {result}"



def test_read_empty_string():
    """测试空字符串"""
    manager = EnvManager()
    result = manager.read_from_string("")
    assert result == {}


def test_skip_comments():
    """测试跳过注释行"""
    manager = EnvManager()
    env_content = """
    # 这是注释
    API_KEY=sk-123456
    # 另一条注释
    DEBUG=True
    """
    expected = {
        'API_KEY': 'sk-123456',
        'DEBUG': 'True'
    }
    result = manager.read_from_string(env_content)
    assert result == expected

def test_handle_spaces():
    """测试处理空格"""
    manager = EnvManager()
    env_content = """
    API_KEY = sk-123456  
    DEBUG  =  True
    """
    expected = {
        'API_KEY': 'sk-123456',
        'DEBUG': 'True'
    }
    result = manager.read_from_string(env_content)
    assert result == expected


def test_handle_missing_value():
    """测试处理缺失值的情况"""
    manager = EnvManager()
    env_content = "API_KEY=\nDEBUG=True\n"
    expected = {
        'API_KEY': '',
        'DEBUG': 'True'
    }
    result = manager.read_from_string(env_content)
    assert result == expected

def test_read_from_file():
    """测试从文件读取"""
    import os
    
    # 创建临时文件
    temp_file = '/tmp/test.env'
    with open(temp_file, 'w') as f:
        f.write("API_KEY=sk-123456\nDEBUG=True\n")
    
    manager = EnvManager()
    result = manager.read_from_file(temp_file)
    
    # 清理
    os.remove(temp_file)
    
    expected = {
        'API_KEY': 'sk-123456',
        'DEBUG': 'True'
    }
    assert result == expected

def test_export_to_string():
    """测试导出为字符串"""
    manager = EnvManager()
    env_dict = {'API_KEY': 'sk-123456', 'DEBUG': 'True'}
    
    result = manager.export_to_string(env_dict)
    
    expected = """
    API_KEY=sk-123456
    DEBUG=True
    """
    # 注意：导出的字符串应该与预期格式匹配
    lines = result.strip().split('\n')
    assert len(lines) == 2
    assert 'API_KEY=sk-123456' in result
    assert 'DEBUG=True' in result

def test_export_empty_dict():
    """测试导出空字典"""
    manager = EnvManager()
    result = manager.export_to_string({})
    assert result.strip() == ''

def test_export_with_comments():
    """测试导出时添加注释"""
    manager = EnvManager()
    env_dict = {'API_KEY': 'sk-123456'}
    
    result = manager.export_to_string(env_dict)
    
    assert 'API_KEY=' in result
    assert '=' in result