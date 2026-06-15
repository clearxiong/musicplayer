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
    config.should_show_today_tokens.return_value = True
    config.should_show_balance.return_value = True
    config.should_show_last_update.return_value = True

    window = UsageWindow(config)
    assert window.windowTitle() == "DeepSeek 使用量监控"
    assert window.windowFlags() & Qt.WindowStaysOnTopHint

def test_window_update_data(app):
    config = Mock(spec=ConfigManager)
    config.get_window_size.return_value = (300, 150)
    config.is_always_on_top.return_value = True
    config.should_show_today_tokens.return_value = True
    config.should_show_balance.return_value = True
    config.should_show_last_update.return_value = True

    window = UsageWindow(config)
    data = UsageData(
        today_tokens=12345,
        balance=98.76,
        last_update="2026-06-15 16:30:00"
    )

    window.update_data(data)
    assert "12,345" in window.tokens_label.text()
    assert "98.76" in window.balance_label.text()
