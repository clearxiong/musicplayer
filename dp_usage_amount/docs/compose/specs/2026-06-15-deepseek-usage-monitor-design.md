# DeepSeek 使用量监控小程序设计文档

## [S1] 问题

用户需要一个Windows小程序来显示DeepSeek API的使用量信息，主要包括今日token用量和余额剩余情况。要求窗口置顶显示，界面内容可配置，数据定时更新。

## [S2] 解决方案概述

开发一个Python + PyQt应用程序，通过DeepSeek API获取使用量数据，以可配置的界面显示在置顶小窗口中。采用模块化设计，配置文件使用YAML格式。

## [S3] 架构设计

### 项目结构
```
dp_usage_amount/
├── main.py          # 应用入口和窗口管理
├── ui.py            # PyQt界面组件
├── api.py           # DeepSeek API调用
├── config.py        # YAML配置文件读写
├── data.py          # 使用量数据模型
├── config.yaml      # 配置文件
└── requirements.txt # 依赖包
```

### 模块职责
1. **main.py**: 应用初始化、窗口创建、定时刷新管理
2. **ui.py**: PyQt界面组件，包括主窗口、标签显示
3. **api.py**: DeepSeek API调用，获取使用量数据
4. **config.py**: 读写YAML配置文件，管理API密钥和显示选项
5. **data.py**: 定义使用量数据模型，解析API响应

### 数据流
```
config.yaml -> config.py -> api.py -> data.py -> ui.py -> 显示
```

## [S4] 界面设计

### 主窗口
- 可调整大小的小窗口
- 置顶显示（始终在最前面）
- 包含两个标签：今日token用量和余额
- 数字显示数据

### 界面元素
1. **今日token用量标签**: 显示当日消耗的token总数
2. **余额标签**: 显示账户剩余余额
3. **刷新时间显示**: 显示最后更新时间

### 样式
- 简洁现代的界面
- 适当的字体大小和颜色
- 响应式布局，适应窗口大小调整

## [S5] API集成

### DeepSeek API
- 使用DeepSeek官方API获取使用量数据
- 需要API密钥认证
- 获取今日token用量和余额信息

### API调用流程
1. 从配置文件读取API密钥
2. 发送请求到DeepSeek API
3. 解析响应数据
4. 更新界面显示

### 错误处理
- API调用失败时显示错误信息
- 网络连接异常处理
- API密钥验证失败处理

## [S6] 配置管理

### 配置文件格式 (YAML)
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

### 配置项说明
1. **api**: API密钥和基础URL
2. **display**: 显示选项，控制显示哪些信息
3. **refresh**: 刷新设置，包括间隔和自动刷新
4. **window**: 窗口设置，包括大小和置顶状态

## [S7] 定时更新

### 刷新机制
- 根据配置文件中的间隔定时刷新
- 支持手动刷新
- 自动刷新可配置开启/关闭

### 更新流程
1. 定时器触发更新
2. 调用API获取最新数据
3. 解析并更新界面显示
4. 更新最后刷新时间

## [S8] 错误处理

### 错误类型
1. **网络错误**: 网络连接失败
2. **API错误**: API调用失败或返回错误
3. **配置错误**: 配置文件格式错误或缺少必要字段
4. **数据错误**: API响应格式不符合预期

### 错误显示
- 在界面上显示简洁的错误信息
- 保持界面美观，不影响用户体验
- 提供重试机制

## [S9] 测试策略

### 单元测试
- 测试配置文件读写
- 测试API调用和数据解析
- 测试数据模型

### 集成测试
- 测试完整数据流
- 测试界面更新
- 测试定时刷新

### 手动测试
- 测试窗口置顶功能
- 测试配置修改
- 测试不同屏幕尺寸下的显示效果

## [S10] 部署和分发

### 依赖管理
- 使用requirements.txt管理Python依赖
- 主要依赖：PyQt5, requests, pyyaml

### 打包
- 可以使用PyInstaller打包为可执行文件
- 包含所有依赖和配置文件

### 安装
- 用户下载后直接运行
- 首次运行时提示配置API密钥