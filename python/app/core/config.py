from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")
    
    APP_NAME: str = "MKIT API"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str


settings = Settings()
