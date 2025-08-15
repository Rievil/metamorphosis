from fastapi import FastAPI
from .db import engine
from .models import Base
from .auth import router as auth_router
from .users import role_router, user_router
from .routes.sessions import router as session_router
from .routes.world_environments import router as world_environment_router
from .routes.archetypes import router as archetype_router
from .routes.skills import router as skill_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(role_router)
app.include_router(session_router)
app.include_router(world_environment_router)
app.include_router(archetype_router)
app.include_router(skill_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}
