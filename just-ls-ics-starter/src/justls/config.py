from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ics_simulator: bool = True
    influx_url: str = "http://localhost:8181"
    influx_token: str = ""
    influx_org: str = "just-lab"
    influx_bucket: str = "ics"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", case_sensitive=False)

settings = Settings()
