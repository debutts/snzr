# snzr backend

python fast api backend

## Quick Startup

run `docker compose up --build`
swagger running at `http://127.0.0.1:8000/docs#/default/root__get`

## Testing

```bash
cd backend
.\.venv\Scripts\python.exe -m pip install -r requirements.txt   # Windows
python -m pytest -v
```


## File Structure

Architecture for a FastAPI app using [Logto](https://logto.io/) for auth and [SQLModel](https://fastapi.tiangolo.com/tutorial/sql-databases/) for persistence, with a clean domain-driven layout.

### Principles

- **Domain-driven**: Each business area (e.g. sneezes, users) lives in its own package with models, schemas, and optional domain logic.
- **Thin routers**: Route modules only handle HTTP and delegate to services or direct DB access.
- **Shared core**: Auth (Logto), DB session, and config are in a central `core` package and injected via FastAPI dependencies.
- **Layered data models**: Per the [FastAPI SQL tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/#create-multiple-models), use a **table model** (SQLModel, `table=True`) for the database and separate **data models** for create/update/response so the API never accepts or exposes internal fields (e.g. server-generated IDs, secrets).

## Resources Used

- <https://fastapi.tiangolo.com/tutorial/sql-databases/#create-an-engine>
- <https://medium.com/@shahpranshu27/connecting-fastapi-to-a-database-using-postgresql-and-sqlmodel-beginner-friendly-guide-52b5aabe6ac3>
- SQL model <https://sqlmodel.tiangolo.com/tutorial/many-to-many/update-remove-relationships/#remove-many-to-many-relationships>
- Testing <https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#fastapi-application>

## Coming Soon

[x] implement tag modification when performing create/update on tags its there its just not working
[x] load in tags
[x] add ability to get sneezes by tag
[x] implement basic testing
[] implement auth for backend (get it testable locally)
[] create basic front end app