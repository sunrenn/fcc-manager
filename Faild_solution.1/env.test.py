import pytest
from unittest.mock import patch

from env import env, load_env, get_env_var, set_env_var, update_from_dict, has_var, reset, load_from_file
from os import environ


def mock_load_from_file():
    return {
        'DB_HOST': 'localhost',
        'DB_PORT': '5432',
        'API_URL': 'https://api.example.com',
    }


@patch('env.load_from_file', mock_load_from_file)
def test_env_var():
    """测试环境变量获取"""
    load_env()
    
    # 测试从配置文件加载
    assert get_env_var('DB_HOST') == 'localhost'
    assert get_env_var('DB_PORT') == '5432'
    assert get_env_var('API_URL') == 'https://api.example.com'
    
    # 测试不存在的环境变量
    assert get_env_var('NON_EXISTENT_VAR') is None


@patch('env.load_from_file', mock_load_from_file)
def test_env_var_default():
    """测试默认值处理"""
    load_env()
    
    # 测试提供默认值
    assert get_env_var('NON_EXISTENT_VAR', 'default_value') == 'default_value'
    assert get_env_var('NON_EXISTENT_VAR', None) is None
    
    # 测试空字符串默认值
    assert get_env_var('NON_EXISTENT_VAR', '') == ''


@patch('env.load_from_file', mock_load_from_file)
def test_update_from_dict():
    """测试批量更新环境变量"""
    load_env()
    
    # 更新环境变量
    new_values = {
        'DB_HOST': 'new-db-host',
        'DB_PORT': '3306',
        'NEW_VAR': 'new_value'
    }
    update_from_dict(new_values)
    
    # 验证更新
    assert get_env_var('DB_HOST') == 'new-db-host'
    assert get_env_var('DB_PORT') == '3306'
    assert get_env_var('NEW_VAR') == 'new_value'


@patch('env.load_from_file', mock_load_from_file)
def test_has_var():
    """测试变量检查"""
    load_env()
    
    # 测试变量存在
    assert has_var('DB_HOST') is True
    assert has_var('NON_EXISTENT_VAR') is False
    
    # 测试使用 set_env_var 设置的变量
    set_env_var('TEST_VAR', 'test_value')
    assert has_var('TEST_VAR') is True
    del environ['TEST_VAR']  # 清理测试环境
    
    # 测试 set_env_var 后立即检查
    set_env_var('TEST_VAR2', 'test_value2')
    assert has_var('TEST_VAR2') is True


@patch('env.load_from_file', mock_load_from_file)
def test_reset():
    """测试重置环境变量"""
    load_env()
    
    # 设置一些测试变量
    set_env_var('TEST_VAR', 'test_value')
    set_env_var('ANOTHER_VAR', 'another_value')
    
    # 重置环境
    reset()
    
    # 验证重置后的状态
    assert get_env_var('TEST_VAR') is None
    assert get_env_var('ANOTHER_VAR') is None
    assert has_var('TEST_VAR') is False
    assert has_var('ANOTHER_VAR') is False
    
    # 验证原始配置仍然可用
    assert get_env_var('DB_HOST') == 'localhost'


@patch('env.load_from_file', mock_load_from_file)
def test_get_all_vars():
    """测试获取所有环境变量"""
    load_env()
    
    # 添加一些测试变量
    set_env_var('VAR_A', 'value_a')
    set_env_var('VAR_B', 'value_b')
    
    # 获取所有变量
    all_vars = env.get_all_vars()
    
    # 验证变量在列表中
    assert 'VAR_A' in all_vars
    assert 'VAR_B' in all_vars
    assert 'DB_HOST' in all_vars
    assert 'DB_PORT' in all_vars
    
    # 验证变量值正确
    assert all_vars['VAR_A'] == 'value_a'
    assert all_vars['VAR_B'] == 'value_b'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
