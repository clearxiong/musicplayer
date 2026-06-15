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
                'key': 'your-api-key-here',
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