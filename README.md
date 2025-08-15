# metamorphosis
Repository for web-based D&D game.

## Database Migrations

Alembic is used for database schema migrations. To apply migrations run:

```
alembic -c backend/alembic.ini upgrade head
```

This command will create or update the database schema to the latest version.
