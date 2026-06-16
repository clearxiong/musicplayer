import pytest
from unittest.mock import Mock, patch
from api import DeepSeekAPI
from data import UsageData

def test_api_initialization():
    api = DeepSeekAPI("test-key", "https://api.test.com")
    assert api.api_key == "test-key"
    assert api.base_url == "https://api.test.com"

@patch('api.requests.get')
def test_api_get_usage_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'is_available': True,
        'balance_infos': [
            {
                'currency': 'CNY',
                'total_balance': '98.76',
                'granted_balance': '0.00',
                'topped_up_balance': '98.76'
            }
        ]
    }
    mock_get.return_value = mock_response
    
    api = DeepSeekAPI("test-key", "https://api.test.com")
    result = api.get_usage()
    
    assert result.balance == 98.76
    assert result.error is None

@patch('api.requests.get')
def test_api_get_usage_network_error(mock_get):
    mock_get.side_effect = Exception("网络连接失败")
    
    api = DeepSeekAPI("test-key", "https://api.test.com")
    result = api.get_usage()
    
    assert result.is_error()
    assert "未知错误" in result.error

@patch('api.requests.get')
def test_api_get_usage_api_error(mock_get):
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.json.return_value = {'error': '无效的API密钥'}
    mock_get.return_value = mock_response
    
    api = DeepSeekAPI("invalid-key", "https://api.test.com")
    result = api.get_usage()
    
    assert result.is_error()
    assert "API错误" in result.error
