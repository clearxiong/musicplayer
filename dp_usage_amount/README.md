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