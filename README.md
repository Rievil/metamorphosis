# metamorphosis
Repository for web-based D&D game.

## Database Migrations

Alembic is used for database schema migrations. To apply migrations run:

```
alembic -c backend/alembic.ini upgrade head
```

This command will create or update the database schema to the latest version.

## Docker Deployment

1. Copy `.env.example` to `.env` and adjust the values for your environment.
2. Build the backend image for your platform:
   - **x86_64 (macOS/Intel):**
     ```bash
     docker buildx build --platform linux/amd64 -t metamorphosis-backend .
     ```
   - **ARM (Raspberry Pi):**
     ```bash
     docker buildx build --platform linux/arm64 -t metamorphosis-backend .
     ```
3. Start the services (backend and PostgreSQL):
   ```bash
   docker compose up
   ```

The backend reads configuration from environment variables:

- `DATABASE_URL` – PostgreSQL connection string constructed from the `POSTGRES_` variables.
- `PORT` – Port FastAPI listens on (default `8000`).
- `SECRET_KEY` – Application secret key.

The provided `docker-compose.yml` links the backend to a Postgres container and exposes the configured ports.
