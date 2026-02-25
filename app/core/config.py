from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "SUPER_SECRET_CHANGE_THIS_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


settings = Settings()
