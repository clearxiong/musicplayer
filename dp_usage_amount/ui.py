from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPainter, QColor, QLinearGradient, QBrush
from config import ConfigManager
from data import UsageData
from api import DeepSeekAPI


class UsageWindow(QMainWindow):
    def __init__(self, config: ConfigManager):
        super().__init__()
        self.config = config
        self.api = DeepSeekAPI(config.get_api_key(), config.get_api_base_url())
        self.initial_balance = None

        self.setup_ui()
        self.setup_timer()
        self.refresh_data()

    def setup_ui(self):
        self.setWindowTitle("DeepSeek 余额监控")
        
        # 设置透明窗口
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 设置窗口标志：无边框 + 置顶
        flags = Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        
        width, height = self.config.get_window_size()
        self.setMinimumSize(width, height)
        self.resize(width, height)

        # 创建central widget
        central_widget = QWidget()
        central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        # 标题
        self.title_label = QLabel("DeepSeek")
        title_font = QFont()
        title_font.setPointSize(10)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: rgba(255,255,255,150); background: transparent;")

        self.balance_label = QLabel("余额: 加载中...")
        self.used_label = QLabel("已使用: --")
        self.update_label = QLabel("最后更新: --")

        # 余额字体更大更粗
        balance_font = QFont()
        balance_font.setPointSize(16)
        balance_font.setBold(True)
        self.balance_label.setFont(balance_font)
        
        used_font = QFont()
        used_font.setPointSize(12)
        self.used_label.setFont(used_font)
        
        small_font = QFont()
        small_font.setPointSize(9)
        self.update_label.setFont(small_font)

        layout.addWidget(self.title_label)
        layout.addSpacing(5)
        layout.addWidget(self.balance_label)
        layout.addWidget(self.used_label)
        layout.addSpacing(10)
        layout.addWidget(self.update_label)

        # 设置标签样式
        self.balance_label.setStyleSheet("color: #ffffff; background: transparent;")
        self.used_label.setStyleSheet("color: rgba(255,255,255,200); background: transparent;")
        self.update_label.setStyleSheet("color: rgba(255,255,255,120); background: transparent;")

    def paintEvent(self, event):
        """绘制半透明渐变背景"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制圆角矩形背景 - 深色半透明渐变
        rect = self.rect()
        
        # 创建渐变效果
        gradient = QLinearGradient(0, 0, 0, rect.height())
        gradient.setColorAt(0, QColor(40, 40, 50, 200))
        gradient.setColorAt(0.5, QColor(30, 30, 40, 210))
        gradient.setColorAt(1, QColor(20, 20, 30, 200))
        
        # 绘制圆角背景
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 12, 12)
        
        # 绘制微妙的边框
        painter.setPen(QColor(255, 255, 255, 30))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 12, 12)
        
        painter.end()

    def mousePressEvent(self, event):
        """允许拖动窗口"""
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """拖动窗口"""
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_pos'):
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

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
            self.used_label.setText("已使用: --")
            self.update_label.setText("最后更新: --")
        else:
            current_balance = data.balance
            
            if self.initial_balance is None:
                self.initial_balance = current_balance
            
            used_amount = self.initial_balance - current_balance
            
            self.balance_label.setText(f"余额: ¥{data.format_balance()}")
            self.used_label.setText(f"已使用: ¥{used_amount:.2f}")
            self.update_label.setText(f"最后更新: {data.last_update}")
