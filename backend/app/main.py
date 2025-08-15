from fastapi import FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from the environment."""

    database_url: str
    secret_key: str

    class Config:
        env_file = ".env"


settings = Settings()

app = FastAPI()


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}
