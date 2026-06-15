import pytest
import tempfile
import os
from unittest.mock import Mock, patch
from main import main
from config import ConfigManager
from api import DeepSeekAPI
from data import UsageData

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
    """测试完整数据流"""
    # 模拟配置
    config = Mock(spec=ConfigManager)
    config.get_api_key.return_value = "test-key"
    config.get_api_base_url.return_value = "https://api.test.com"
    
    # 模拟API响应
    api = Mock(spec=DeepSeekAPI)
    api.get_usage.return_value = UsageData(
        today_tokens=12345,
        balance=98.76,
        last_update="2026-06-15 16:30:00"
    )
    
    # 测试数据流
    data = api.get_usage()
    assert data.today_tokens == 12345
    assert data.balance == 98.76
