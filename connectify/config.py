import os
from dataclasses import dataclass
from typing import Optional

ENV_PREFIX = "CONNECTIFY_"


@dataclass
class Config:
    openweather_api_key: Optional[str] = None
    timeout: int = 10

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            openweather_api_key=os.getenv(f"{ENV_PREFIX}OPENWEATHER_API_KEY"),
            timeout=int(os.getenv(f"{ENV_PREFIX}TIMEOUT", "10")),
        )