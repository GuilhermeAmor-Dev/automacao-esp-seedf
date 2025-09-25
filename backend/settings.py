from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path


def _load_dotenv() -> None:
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key, value)


class Settings:
    def __init__(self) -> None:
        _load_dotenv()
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise RuntimeError(
                "DATABASE_URL environment variable is required to start the API."
            )
        self.secret_key = os.getenv("SECRET_KEY")
        if not self.secret_key:
            raise RuntimeError(
                "SECRET_KEY environment variable is required to sign JWT tokens."
            )
        self.algorithm = os.getenv("ALGORITHM", "HS256")
        expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
        try:
            self.access_token_expire_minutes = int(expire_minutes)
        except ValueError as exc:
            raise RuntimeError(
                "ACCESS_TOKEN_EXPIRE_MINUTES must be an integer"
            ) from exc


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
