from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        str_strip_whitespace=True,
        env_prefix="db_",
    )
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    NAME: str

    @property
    def url_psycopg(self):
        return f"postgresql+psycopg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"

    @property
    def url_asyncpg(self):
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


db_settings = DatabaseSettings()  # type: ignore
