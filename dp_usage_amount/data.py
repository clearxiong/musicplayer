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
