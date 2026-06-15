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
            
        except Exception as e:
            return UsageData.error_state(f"网络错误: {str(e)}")
