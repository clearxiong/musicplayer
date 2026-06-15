import pytest
import tempfile
import os
from config import ConfigManager

def test_config_load():
    """测试配置文件加载"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("""
api:
  key: "test-key"
  base_url: "https://api.test.com"
display:
  show_today_tokens: true
refresh:
  interval_minutes: 10
window:
  width: 400
  height: 200
""")
        temp_path = f.name
    
    try:
        config = ConfigManager(temp_path)
        assert config.get_api_key() == "test-key"
        assert config.get_api_base_url() == "https://api.test.com"
        assert config.get_refresh_interval() == 10
        assert config.get_window_size() == (400, 200)
    finally:
        os.unlink(temp_path)

def test_config_default_values():
    """测试默认配置值"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("api:\n  key: 'test'")
        temp_path = f.name
    
    try:
        config = ConfigManager(temp_path)
        assert config.get_refresh_interval() == 5  # 默认值
        assert config.get_window_size() == (300, 150)  # 默认值
    finally:
        os.unlink(temp_path)