from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        extra="ignore",
    )

    name: str = Field(description="Name project")
    version: str = Field(description="Version project")
    debug: bool = Field(False)
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="DATABASE_",
        extra="ignore",
    )

    driver: str = Field("postgresql+asyncpg", description="Database driver")
    host: str = Field(description="Database host name")
    port: int = Field(description="Database port")
    user: str = Field(description="Database user name")
    password: str = Field(description="Database password")
    name: str = Field(description="Database name")

    @computed_field
    @property
    def database_url(self) -> str:
        return f"{self.driver}://{self.user}:{self.password}" f"@{self.host}:{self.port}/{self.name}"


class SecuritySettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SECURITY_",
        extra="ignore",
    )

    jwt_secret: str = Field(description="JWT secret")
    jwt_algorithm: str = Field(description="HS256")
    jwt_access_ttl_min: int = Field(description="JWT access token TTL")
    jwt_refresh_ttl_days: int = Field(description="JWT refresh token TTL")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    app: AppSettings = Field(default_factory=AppSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)


settings = Settings()
