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
        self.initial_balance = None  # 记录初始余额

        self.setup_ui()
        self.setup_timer()
        self.refresh_data()

    def setup_ui(self):
        self.setWindowTitle("DeepSeek 余额监控")
        width, height = self.config.get_window_size()
        self.setMinimumSize(width, height)
        self.resize(width, height)

        if self.config.is_always_on_top():
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)

        self.balance_label = QLabel("余额: 加载中...")
        self.used_label = QLabel("已使用: --")
        self.update_label = QLabel("最后更新: --")

        font = QFont()
        font.setPointSize(12)
        self.balance_label.setFont(font)
        self.used_label.setFont(font)
        self.update_label.setFont(font)

        layout.addWidget(self.balance_label)
        layout.addWidget(self.used_label)
        layout.addWidget(self.update_label)

        self.setStyleSheet("""
            QMainWindow {
                background-color: rgba(30, 30, 30, 180);
            }
            QLabel {
                color: #ffffff;
                padding: 8px;
                font-size: 14px;
            }
        """)
        
        # 设置窗口透明
        self.setAttribute(Qt.WA_TranslucentBackground)

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
            self.balance_label.setText(f"错误: {data.error}")
            self.used_label.setText("已使用: N/A")
            self.update_label.setText("最后更新: --")
        else:
            current_balance = data.balance
            
            # 记录第一次查询的余额作为初始值
            if self.initial_balance is None:
                self.initial_balance = current_balance
            
            # 计算已使用金额
            used_amount = self.initial_balance - current_balance
            
            self.balance_label.setText(f"余额: ¥{data.format_balance()}")
            self.used_label.setText(f"已使用: ¥{used_amount:.2f}")
            self.update_label.setText(f"最后更新: {data.last_update}")
