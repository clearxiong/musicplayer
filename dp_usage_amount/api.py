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
                'Accept': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            
            response = requests.get(
                f"{self.base_url}/user/balance",
                headers=headers,
                timeout=10
            )
            
            if response.status_code != 200:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', '未知错误')
                except:
                    error_msg = f"HTTP {response.status_code}"
                return UsageData.error_state(f"API错误: {error_msg}")
            
            data = response.json()
            
            # 根据DeepSeek API响应格式解析数据
            # 响应格式: {"is_available": true, "balance_infos": [{"currency": "CNY", "total_balance": "96.39", ...}]}
            balance_infos = data.get('balance_infos', [])
            
            balance = 0.0
            if balance_infos:
                balance = float(balance_infos[0].get('total_balance', 0.0))
            
            return UsageData(
                today_tokens=0,  # 此API不提供今日token用量
                balance=balance,
                last_update=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
        except requests.exceptions.RequestException as e:
            return UsageData.error_state(f"网络错误: {str(e)}")
        except Exception as e:
            return UsageData.error_state(f"未知错误: {str(e)}")
