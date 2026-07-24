from pydantic_settings import BaseSettings, SettingsConfigDict

class Configuraciones(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    CLAVE_SECRETA: str
    ALGORITMO: str = "HS256"
    MINUTOS_EXPIRACION_TOKEN: int = 60

    @property
    def url_base_datos(self):
        return (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

configuraciones = Configuraciones()