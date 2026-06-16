# DeepSeek 使用量监控小程序实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use compose:subagent (recommended) or compose:execute to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 开发一个Python + PyQt应用程序，通过DeepSeek API获取使用量数据，以可配置的界面显示在置顶小窗口中。

**Architecture:** 模块化设计，分为5个主要模块：main.py（应用入口）、ui.py（界面）、api.py（API调用）、config.py（配置管理）、data.py（数据模型）。使用YAML配置文件存储设置，PyQt5实现界面，requests调用API。

**Tech Stack:** Python 3.8+, PyQt5, requests, pyyaml

---

### Task 1: 项目初始化和依赖管理

**Covers:** [S3, S10]
<!-- 架构设计和部署分发 -->

**Files:**
- Create: `requirements.txt`
- Create: `config.yaml`
- Create: `main.py`

- [ ] **Step 1: 创建requirements.txt**

```
PyQt5>=5.15.0
requests>=2.28.0
pyyaml>=6.0
```

- [ ] **Step 2: 创建config.yaml**

```yaml
api:
  key: "your-api-key-here"
  base_url: "https://api.deepseek.com"

display:
  show_today_tokens: true
  show_balance: true
  show_last_update: true

refresh:
  interval_minutes: 5
  auto_refresh: true

window:
  width: 300
  height: 150
  always_on_top: true
```

- [ ] **Step 3: 创建main.py（基础框架）**

```python
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from config import ConfigManager
from ui import UsageWindow

def main():
    # 初始化配置
    config = ConfigManager()
    
    # 创建应用
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # 创建主窗口
    window = UsageWindow(config)
    window.show()
    
    # 运行应用
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 测试基础框架**

Run: `python main.py`
Expected: 应用启动但显示错误（因为缺少模块）

- [ ] **Step 5: 提交初始项目结构**

```bash
git add requirements.txt config.yaml main.py
git commit -m "feat: 初始化项目结构和配置文件"
```

### Task 2: 配置管理模块

**Covers:** [S6]
<!-- 配置管理 -->

**Files:**
- Create: `config.py`
- Test: `tests/test_config.py`

- [ ] **Step 1: 编写配置管理测试**

```python
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
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_config.py -v`
Expected: FAIL（因为config.py不存在）

- [ ] **Step 3: 实现ConfigManager类**

```python
import yaml
import os

class ConfigManager:
    def __init__(self, config_path="config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self):
        if not os.path.exists(self.config_path):
            return self._get_default_config()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config or self._get_default_config()
        except Exception:
            return self._get_default_config()
    
    def _get_default_config(self):
        return {
            'api': {
                'key': '',
                'base_url': 'https://api.deepseek.com'
            },
            'display': {
                'show_today_tokens': True,
                'show_balance': True,
                'show_last_update': True
            },
            'refresh': {
                'interval_minutes': 5,
                'auto_refresh': True
            },
            'window': {
                'width': 300,
                'height': 150,
                'always_on_top': True
            }
        }
    
    def get_api_key(self):
        return self.config.get('api', {}).get('key', '')
    
    def get_api_base_url(self):
        return self.config.get('api', {}).get('base_url', 'https://api.deepseek.com')
    
    def get_refresh_interval(self):
        return self.config.get('refresh', {}).get('interval_minutes', 5)
    
    def get_window_size(self):
        width = self.config.get('window', {}).get('width', 300)
        height = self.config.get('window', {}).get('height', 150)
        return (width, height)
    
    def is_always_on_top(self):
        return self.config.get('window', {}).get('always_on_top', True)
    
    def should_show_today_tokens(self):
        return self.config.get('display', {}).get('show_today_tokens', True)
    
    def should_show_balance(self):
        return self.config.get('display', {}).get('show_balance', True)
    
    def should_show_last_update(self):
        return self.config.get('display', {}).get('show_last_update', True)
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_config.py -v`
Expected: PASS

- [ ] **Step 5: 提交配置管理模块**

```bash
git add config.py tests/test_config.py
git commit -m "feat: 实现配置管理模块"
```

### Task 3: 数据模型模块

**Covers:** [S3]
<!-- 架构设计 -->

**Files:**
- Create: `data.py`
- Test: `tests/test_data.py`

- [ ] **Step 1: 编写数据模型测试**

```python
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
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_data.py -v`
Expected: FAIL（因为data.py不存在）

- [ ] **Step 3: 实现UsageData类**

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class UsageData:
    today_tokens: Optional[int]
    balance: Optional[float]
    last_update: str
    error: Optional[str] = None
    
    @classmethod
    def error_state(cls, error_message: str):
        return cls(
            today_tokens=None,
            balance=None,
            last_update="",
            error=error_message
        )
    
    def format_tokens(self) -> str:
        if self.today_tokens is None:
            return "N/A"
        return f"{self.today_tokens:,}"
    
    def format_balance(self) -> str:
        if self.balance is None:
            return "N/A"
        return f"{self.balance:.2f}"
    
    def is_error(self) -> bool:
        return self.error is not None
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_data.py -v`
Expected: PASS

- [ ] **Step 5: 提交数据模型模块**

```bash
git add data.py tests/test_data.py
git commit -m "feat: 实现数据模型模块"
```

### Task 4: API调用模块

**Covers:** [S5]
<!-- API集成 -->

**Files:**
- Create: `api.py`
- Test: `tests/test_api.py`

- [ ] **Step 1: 编写API调用测试**

```python
import pytest
from unittest.mock import Mock, patch
from api import DeepSeekAPI
from data import UsageData

def test_api_initialization():
    """测试API初始化"""
    api = DeepSeekAPI("test-key", "https://api.test.com")
    assert api.api_key == "test-key"
    assert api.base_url == "https://api.test.com"

@patch('api.requests.get')
def test_api_get_usage_success(mock_get):
    """测试API成功获取使用量"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'data': {
            'today_tokens': 12345,
            'balance': 98.76
        }
    }
    mock_get.return_value = mock_response
    
    api = DeepSeekAPI("test-key", "https://api.test.com")
    result = api.get_usage()
    
    assert result.today_tokens == 12345
    assert result.balance == 98.76
    assert result.error is None

@patch('api.requests.get')
def test_api_get_usage_network_error(mock_get):
    """测试网络错误"""
    mock_get.side_effect = Exception("网络连接失败")
    
    api = DeepSeekAPI("test-key", "https://api.test.com")
    result = api.get_usage()
    
    assert result.is_error()
    assert "网络错误" in result.error

@patch('api.requests.get')
def test_api_get_usage_api_error(mock_get):
    """测试API返回错误"""
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.json.return_value = {'error': '无效的API密钥'}
    mock_get.return_value = mock_response
    
    api = DeepSeekAPI("invalid-key", "https://api.test.com")
    result = api.get_usage()
    
    assert result.is_error()
    assert "API错误" in result.error
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_api.py -v`
Expected: FAIL（因为api.py不存在）

- [ ] **Step 3: 实现DeepSeekAPI类**

```python
import requests
from datetime import datetime
from data import UsageData

class DeepSeekAPI:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
    
    def get_usage(self) -> UsageData:
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.base_url}/v1/usage",
                headers=headers,
                timeout=10
            )
            
            if response.status_code != 200:
                error_data = response.json()
                return UsageData.error_state(f"API错误: {error_data.get('error', '未知错误')}")
            
            data = response.json()
            usage_data = data.get('data', {})
            
            return UsageData(
                today_tokens=usage_data.get('today_tokens', 0),
                balance=usage_data.get('balance', 0.0),
                last_update=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
        except requests.exceptions.RequestException as e:
            return UsageData.error_state(f"网络错误: {str(e)}")
        except Exception as e:
            return UsageData.error_state(f"未知错误: {str(e)}")
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_api.py -v`
Expected: PASS

- [ ] **Step 5: 提交API调用模块**

```bash
git add api.py tests/test_api.py
git commit -m "feat: 实现API调用模块"
```

### Task 5: 界面模块

**Covers:** [S4]
<!-- 界面设计 -->

**Files:**
- Create: `ui.py`
- Test: `tests/test_ui.py`

- [ ] **Step 1: 编写界面测试**

```python
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
    """测试窗口创建"""
    config = Mock(spec=ConfigManager)
    config.get_window_size.return_value = (300, 150)
    config.is_always_on_top.return_value = True
    config.should_show_today_tokens.return_value = True
    config.should_show_balance.return_value = True
    config.should_show_last_update.return_value = True
    
    window = UsageWindow(config)
    assert window.windowTitle() == "DeepSeek 使用量监控"
    assert window.isWindowFlag(Qt.WindowStaysOnTopHint)

def test_window_update_data(app):
    """测试窗口数据更新"""
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
```

- [ ] **Step 2: 运行测试确认失败**

Run: `pytest tests/test_ui.py -v`
Expected: FAIL（因为ui.py不存在）

- [ ] **Step 3: 实现UsageWindow类**

```python
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
        # 窗口设置
        self.setWindowTitle("DeepSeek 使用量监控")
        width, height = self.config.get_window_size()
        self.setFixedSize(width, height)
        
        # 置顶设置
        if self.config.is_always_on_top():
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        # 创建主部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建标签
        self.tokens_label = QLabel("今日token: 加载中...")
        self.balance_label = QLabel("余额: 加载中...")
        self.update_label = QLabel("最后更新: --")
        
        # 设置字体
        font = QFont()
        font.setPointSize(10)
        self.tokens_label.setFont(font)
        self.balance_label.setFont(font)
        self.update_label.setFont(font)
        
        # 添加标签到布局
        layout.addWidget(self.tokens_label)
        layout.addWidget(self.balance_label)
        layout.addWidget(self.update_label)
        
        # 设置窗口样式
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
        # 创建定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_data)
        
        # 设置定时器间隔
        interval_minutes = self.config.get_refresh_interval()
        self.timer.start(interval_minutes * 60 * 1000)  # 转换为毫秒
    
    def refresh_data(self):
        # 获取最新数据
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
```

- [ ] **Step 4: 运行测试确认通过**

Run: `pytest tests/test_ui.py -v`
Expected: PASS

- [ ] **Step 5: 提交界面模块**

```bash
git add ui.py tests/test_ui.py
git commit -m "feat: 实现界面模块"
```

### Task 6: 集成测试和最终验证

**Covers:** [S9]
<!-- 测试策略 -->

**Files:**
- Test: `tests/test_integration.py`

- [ ] **Step 1: 编写集成测试**

```python
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
```

- [ ] **Step 2: 运行所有测试**

Run: `pytest tests/ -v`
Expected: 所有测试通过

- [ ] **Step 3: 测试应用启动**

Run: `python main.py`
Expected: 应用正常启动，显示界面（可能显示API错误，因为没有真实密钥）

- [ ] **Step 4: 提交集成测试**

```bash
git add tests/test_integration.py
git commit -m "feat: 添加集成测试"
```

### Task 7: 文档和最终提交

**Covers:** [S10]
<!-- 部署和分发 -->

**Files:**
- Create: `README.md`

- [ ] **Step 1: 创建README.md**

```markdown
# DeepSeek 使用量监控小程序

一个Windows小程序，用于显示DeepSeek API的使用量信息。

## 功能

- 显示今日token用量
- 显示账户余额
- 窗口置顶显示
- 定时自动刷新
- 可配置显示内容

## 安装

1. 克隆仓库
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 配置API密钥：
   编辑 `config.yaml` 文件，填入你的DeepSeek API密钥

## 使用

运行程序：
```bash
python main.py
```

## 配置

编辑 `config.yaml` 文件：

```yaml
api:
  key: "your-api-key-here"  # 你的API密钥
  base_url: "https://api.deepseek.com"  # API地址

display:
  show_today_tokens: true  # 显示今日token用量
  show_balance: true  # 显示余额
  show_last_update: true  # 显示最后更新时间

refresh:
  interval_minutes: 5  # 刷新间隔（分钟）
  auto_refresh: true  # 自动刷新

window:
  width: 300  # 窗口宽度
  height: 150  # 窗口高度
  always_on_top: true  # 窗口置顶
```

## 依赖

- PyQt5
- requests
- pyyaml
```

- [ ] **Step 2: 最终提交**

```bash
git add README.md
git commit -m "docs: 添加项目README文档"
```

- [ ] **Step 3: 运行完整测试套件**

Run: `pytest tests/ -v`
Expected: 所有测试通过

- [ ] **Step 4: 验证应用功能**

Run: `python main.py`
Expected: 应用正常启动，显示配置界面

- [ ] **Step 5: 最终代码检查**

```bash
git status
git log --oneline -5
```

检查所有文件已提交，没有未跟踪的文件。