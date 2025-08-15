from fastapi import FastAPI
from .db import engine
from .models import Base
from .auth import router as auth_router
from .users import role_router, user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(role_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}
