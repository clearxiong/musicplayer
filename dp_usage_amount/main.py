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
    
    # 创建主窗口
    window = UsageWindow(config)
    window.show()
    
    # 运行应用
    sys.exit(app.exec_())

if __name__ == "__main__":
    # import requests

    # url = "https://api.deepseek.com/user/balance"

    # payload={}
    # headers = {
    #   'Accept': 'application/json',
    #   'Authorization': 'Bearer sk-a30fe490393a4d2c9276d0ac44e8c685'
    # }

    # response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)    
    main()
