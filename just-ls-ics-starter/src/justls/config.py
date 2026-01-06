from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]  # -> just-ls-ics-starter
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    run_mode: Literal["sim", "hw"] = "sim"

    influx_url: str = "http://localhost:8181"
    influx_token: str = ""
    influx_org: str = "just-lab"
    influx_bucket: str = "ics"
    telemetry_enabled: bool = False
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_prefix="",            
        case_sensitive=False,
    )


settings = Settings()
