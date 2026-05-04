"""Environment-backed runtime settings."""

from dataclasses import dataclass
from functools import lru_cache
import os
import warnings

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    sendgrid_api_key: str
    sender_email: str
    recipient_email: str
    planner_search_count: int


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        warnings.warn(f"Missing required environment variable: {name}", stacklevel=2)
        return ""
    print(f"{name} is present")
    return value


@lru_cache(maxsize=1)
def load_settings(load_dotenv_file: bool = True) -> Settings:
    if load_dotenv_file:
        load_dotenv(override=False)

    planner_search_count_raw = os.getenv("PLANNER_SEARCH_COUNT", "5")
    try:
        planner_search_count = int(planner_search_count_raw)
    except ValueError:
        warnings.warn(
            "Invalid PLANNER_SEARCH_COUNT; falling back to 5",
            stacklevel=2,
        )
        planner_search_count = 5

    return Settings(
        openai_api_key=_require_env("OPENAI_API_KEY"),
        sendgrid_api_key=_require_env("SENDGRID_API_KEY"),
        sender_email=os.getenv("SENDER_EMAIL", "<REPLACE WITH YOUR SENDER EMAIL>"),
        recipient_email=os.getenv("RECIPIENT_EMAIL", "<REPLACE WITH YOUR RECIPIENT EMAIL>"),
        planner_search_count=planner_search_count,
    )
