import pytest
from data import UsageData

def test_usage_data_creation():
    """测试UsageData创建"""
    data = UsageData(
        today_tokens=12345,
        balance=98.76,
        last_update="2026-06-15 16:30:00"
    )
    
    assert data.today_tokens == 12345
    assert data.balance == 98.76
    assert data.last_update == "2026-06-15 16:30:00"

def test_usage_data_format_tokens():
    """测试token格式化"""
    data = UsageData(today_tokens=12345678, balance=100.0, last_update="")
    assert data.format_tokens() == "12,345,678"

def test_usage_data_format_balance():
    """测试余额格式化"""
    data = UsageData(today_tokens=0, balance=98.765, last_update="")
    assert data.format_balance() == "98.77"

def test_usage_data_error_state():
    """测试错误状态"""
    data = UsageData.error_state("网络错误")
    assert data.today_tokens is None
    assert data.balance is None
    assert data.error == "网络错误"