import ctypes
from ctypes import wintypes
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from config import ConfigManager
from data import UsageData
from api import DeepSeekAPI

# Windows API 常量
DWMWA_USE_IMMERSIVE_DARK_MODE = 20
DWMWA_SYSTEMBACKDROP_TYPE = 38
DWMSBT_MAINWINDOW = 2  # 毛玻璃效果

# 加载 dwmapi
dwmapi = ctypes.windll.dwmapi


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
        
        # 设置窗口标志：无边框 + 置顶
        flags = Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        
        # 启用鼠标事件穿透（可选，允许点击穿透）
        # self.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        width, height = self.config.get_window_size()
        self.setMinimumSize(width, height)
        self.resize(width, height)

        # 创建central widget
        central_widget = QWidget()
        central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        self.balance_label = QLabel("余额: 加载中...")
        self.used_label = QLabel("已使用: --")
        self.update_label = QLabel("最后更新: --")

        font = QFont()
        font.setPointSize(12)
        self.balance_label.setFont(font)
        self.used_label.setFont(font)
        
        small_font = QFont()
        small_font.setPointSize(9)
        self.update_label.setFont(small_font)

        layout.addWidget(self.balance_label)
        layout.addWidget(self.used_label)
        layout.addSpacing(10)
        layout.addWidget(self.update_label)

        # 设置标签样式 - 白色文字，透明背景
        self.balance_label.setStyleSheet("color: #ffffff; background: transparent; font-weight: bold;")
        self.used_label.setStyleSheet("color: #ffffff; background: transparent;")
        self.update_label.setStyleSheet("color: #cccccc; background: transparent;")

        # 应用毛玻璃效果
        self.apply_acrylic_effect()

    def apply_acrylic_effect(self):
        """应用Windows毛玻璃/亚克力效果"""
        hwnd = int(self.winId())
        
        # 设置深色模式
        dark_mode = ctypes.c_int(1)
        dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(dark_mode),
            ctypes.sizeof(dark_mode)
        )
        
        # 设置亚克力/毛玻璃背景
        backdrop_type = ctypes.c_int(DWMSBT_MAINWINDOW)
        dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_SYSTEMBACKDROP_TYPE,
            ctypes.byref(backdrop_type),
            ctypes.sizeof(backdrop_type)
        )
        
        # 扩展窗口边框到客户区（使效果覆盖整个窗口）
        class MARGINS(ctypes.Structure):
            _fields_ = [
                ("cxLeftWidth", ctypes.c_int),
                ("cxRightWidth", ctypes.c_int),
                ("cyTopHeight", ctypes.c_int),
                ("cyBottomHeight", ctypes.c_int),
            ]
        
        margins = MARGINS(-1, -1, -1, -1)  # -1 表示扩展到整个窗口
        dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(margins))

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
