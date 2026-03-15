# snzr backend

python fast api backend

## Quick Startup

**Python API:** `uvicorn main:app --reload` (from project root).

## File Structure

Architecture for a FastAPI app using [Logto](https://logto.io/) for auth and [SQLModel](https://fastapi.tiangolo.com/tutorial/sql-databases/) for persistence, with a clean domain-driven layout.

### Principles

- **Domain-driven**: Each business area (e.g. sneezes, users) lives in its own package with models, schemas, and optional domain logic.
- **Thin routers**: Route modules only handle HTTP and delegate to services or direct DB access.
- **Shared core**: Auth (Logto), DB session, and config are in a central `core` package and injected via FastAPI dependencies.
- **Layered data models**: Per the [FastAPI SQL tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/#create-multiple-models), use a **table model** (SQLModel, `table=True`) for the database and separate **data models** for create/update/response so the API never accepts or exposes internal fields (e.g. server-generated IDs, secrets).

### Persistence (SQLModel)

- One **engine** in **core/db.py** (e.g. SQLite for dev, PostgreSQL for prod via `config.DATABASE_URL`).
- One **session per request** via `get_session()` with `yield`, and `SessionDep = Annotated[Session, Depends(get_session)]`.
- Table models in **domains/\*/models.py**; create tables on startup with `SQLModel.metadata.create_all(engine)`.
- For create: accept `SneezeCreate`, build `Sneeze` (table) with `Sneeze.model_validate(create_model)` and set `user_id` from `get_current_user`; for update use `model_dump(exclude_unset=True)` and `sqlmodel_update` for partial updates.

This layout keeps domains isolated, auth and DB in one place, and aligns with [FastAPI’s SQL tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/) and [Logto](https://logto.io/) for a scalable, maintainable API.

## Resources Used

### DB

- <https://fastapi.tiangolo.com/tutorial/sql-databases/#create-an-engine>
- <https://medium.com/@shahpranshu27/connecting-fastapi-to-a-database-using-postgresql-and-sqlmodel-beginner-friendly-guide-52b5aabe6ac3>
