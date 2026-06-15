import pytest
import tempfile
import os
from config import ConfigManager
from api import DeepSeekAPI

def test_config_api_integration():
    """测试配置和API集成"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("""
api:
  key: "integration-test-key"
  base_url: "https://api.integration-test.com"
refresh:
  interval_minutes: 1
""")
        temp_path = f.name
    
    try:
        config = ConfigManager(temp_path)
        api = DeepSeekAPI(config.get_api_key(), config.get_api_base_url())
        
        assert api.api_key == "integration-test-key"
        assert api.base_url == "https://api.integration-test.com"
    finally:
        os.unlink(temp_path)

def test_data_flow():
    """测试完整数据流（真实组件）"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("""
api:
  key: "test-key"
  base_url: "https://api.test.com"
refresh:
  interval_minutes: 1
""")
        temp_path = f.name
    
    try:
        config = ConfigManager(temp_path)
        api = DeepSeekAPI(config.get_api_key(), config.get_api_base_url())
        
        assert api.api_key == "test-key"
        assert api.base_url == "https://api.test.com"
    finally:
        os.unlink(temp_path)

def test_app_initialization():
    """测试应用初始化"""
    config = ConfigManager()
    assert config.get_api_key() is not None
    assert config.get_api_base_url() is not None
    assert config.get_refresh_interval() > 0
    assert config.get_window_size() == (300, 150)

def test_config_error_handling():
    """测试配置错误处理"""
    config = ConfigManager("nonexistent.yaml")
    assert config.get_api_key() == "your-api-key-here"
    assert config.get_api_base_url() == "https://api.deepseek.com"

def test_api_error_handling():
    """测试API错误处理"""
    api = DeepSeekAPI("invalid-key", "https://api.test.com")
    assert api.api_key == "invalid-key"
