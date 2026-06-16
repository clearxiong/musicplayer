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

    @classmethod
    def from_api_response(cls, response: dict):
        """从API响应字典创建UsageData实例"""
        try:
            if not isinstance(response, dict):
                raise ValueError("响应不是字典类型")
            data = response.get('data')
            if not isinstance(data, dict):
                raise ValueError("响应中缺少'data'字段或'data'不是字典")
            return cls(
                today_tokens=data.get('today_tokens', 0),
                balance=data.get('balance', 0.0),
                last_update=data.get('last_update', '')
            )
        except Exception as e:
            return cls.error_state(f"解析API响应失败: {str(e)}")

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
