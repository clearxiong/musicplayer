from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from config import ConfigManager
from data import UsageData
from api import DeepSeekAPI


class UsageWindow(QMainWindow):
    def __init__(self, config: ConfigManager):
        super().__init__()
        self.config = config
        self.api = DeepSeekAPI(config.get_api_key(), config.get_api_base_url())

        self.setup_ui()
        self.setup_timer()
        self.refresh_data()

    def setup_ui(self):
        self.setWindowTitle("DeepSeek 使用量监控")
        width, height = self.config.get_window_size()
        self.setFixedSize(width, height)

        if self.config.is_always_on_top():
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)

        self.tokens_label = QLabel("今日token: 加载中...")
        self.balance_label = QLabel("余额: 加载中...")
        self.update_label = QLabel("最后更新: --")

        font = QFont()
        font.setPointSize(10)
        self.tokens_label.setFont(font)
        self.balance_label.setFont(font)
        self.update_label.setFont(font)

        layout.addWidget(self.tokens_label)
        layout.addWidget(self.balance_label)
        layout.addWidget(self.update_label)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #333;
                padding: 5px;
            }
        """)

    def setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_data)
        try:
            interval_minutes = self.config.get_refresh_interval()
            self.timer.start(int(interval_minutes * 60 * 1000))
        except Exception:
            self.timer.start(5 * 60 * 1000)

    def refresh_data(self):
        data = self.api.get_usage()
        self.update_data(data)

    def update_data(self, data: UsageData):
        if data.is_error():
            self.tokens_label.setText(f"错误: {data.error}")
            self.balance_label.setText("余额: N/A")
            self.update_label.setText("最后更新: --")
        else:
            if self.config.should_show_today_tokens():
                self.tokens_label.setText(f"今日token: {data.format_tokens()}")
            else:
                self.tokens_label.setText("")

            if self.config.should_show_balance():
                self.balance_label.setText(f"余额: {data.format_balance()}")
            else:
                self.balance_label.setText("")

            if self.config.should_show_last_update():
                self.update_label.setText(f"最后更新: {data.last_update}")
            else:
                self.update_label.setText("")
