import pytest
from unittest.mock import Mock
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui import UsageWindow
from config import ConfigManager
from data import UsageData

@pytest.fixture
def app():
    return QApplication([])

def test_window_creation(app):
    config = Mock(spec=ConfigManager)
    config.get_window_size.return_value = (300, 150)
    config.is_always_on_top.return_value = True

    window = UsageWindow(config)
    assert window.windowTitle() == "DeepSeek 余额监控"
    assert window.windowFlags() & Qt.WindowStaysOnTopHint

def test_window_update_data(app):
    config = Mock(spec=ConfigManager)
    config.get_window_size.return_value = (300, 150)
    config.is_always_on_top.return_value = True

    window = UsageWindow(config)
    
    # 第一次查询，设置初始余额
    data1 = UsageData(
        today_tokens=0,
        balance=100.0,
        last_update="2026-06-16 12:00:00"
    )
    window.update_data(data1)
    assert "100.00" in window.balance_label.text()
    assert window.initial_balance == 100.0
    
    # 第二次查询，计算已使用金额
    data2 = UsageData(
        today_tokens=0,
        balance=95.5,
        last_update="2026-06-16 12:05:00"
    )
    window.update_data(data2)
    assert "95.50" in window.balance_label.text()
    assert "4.50" in window.used_label.text()  # 100.0 - 95.5 = 4.5

def test_window_resizable(app):
    """测试窗口可以调整大小"""
    config = Mock(spec=ConfigManager)
    config.get_window_size.return_value = (300, 150)
    config.is_always_on_top.return_value = True

    window = UsageWindow(config)

    # 验证窗口可以调整大小
    window.resize(400, 200)
    assert window.width() == 400
    assert window.height() == 200

    # 验证窗口有最小尺寸限制
    window.resize(100, 50)
    assert window.width() >= 300
    assert window.height() >= 150
