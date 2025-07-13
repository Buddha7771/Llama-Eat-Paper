from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    NOTION_TOKEN: str
    NOTION_DATABASE_ID: str
    SLACK_TOKEN: str
    SLACK_CHANNEL_ID: str
    EMBEDDING_MODEL: str = "mxbai-embed-large"


settings = Settings()
