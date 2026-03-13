# snzr

Sneeze Tracking App

## Quick Startup

**Python API:** `uvicorn main:app --reload` (from project root).

### Environment (Logto JWT auth)

The FastAPI app validates `Authorization: Bearer <token>` using Logto’s JWKS. Set:

| Variable | Required | Description |
|----------|----------|-------------|
| `LOGTO_ENDPOINT` | Yes | Logto tenant URL, e.g. `https://your-tenant.logto.app` |
| `LOGTO_API_RESOURCE` | No | API resource indicator (audience). If set, tokens must include this in `aud`. |
| `LOGTO_REQUIRED_SCOPES` | No | Comma-separated scopes required for protected routes, e.g. `api:read,api:write`. |

Your React app should request the same API resource and scopes when getting the access token from Logto so the backend can validate them.

## API

Base URL: `http://localhost:8080`

**Windows PowerShell:** In PowerShell, `curl` is an alias for `Invoke-WebRequest` and uses different syntax. Use **`curl.exe`** for the bash examples below, or use the PowerShell examples in each section.

### List all sneezes

**Bash / Git Bash / WSL:**
```bash
curl http://localhost:8080/sneeze
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri http://localhost:8080/sneeze -Method Get
```

### Get sneeze by ID

**Bash:**
```bash
curl http://localhost:8080/sneeze/1
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri http://localhost:8080/sneeze/1 -Method Get
```

### Create sneeze

**Bash:**
```bash
curl -X POST http://localhost:8080/sneeze \
  -H "Content-Type: application/json" \
  -d "{\"notes\":\"After dusting\",\"location\":\"Bedroom\",\"volume\":2}"
```

**PowerShell:**
```powershell
$body = '{"notes":"After dusting","location":"Bedroom","volume":2}'
Invoke-RestMethod -Uri http://localhost:8080/sneeze -Method Post -Body $body -ContentType "application/json"
```

With optional `occurred_at` (ISO8601), PowerShell:
```powershell
$body = '{"notes":"Pollen","occurred_at":"2025-02-28T14:30:00Z","location":"Garden","volume":3}'
Invoke-RestMethod -Uri http://localhost:8080/sneeze -Method Post -Body $body -ContentType "application/json"
```

### Update sneeze

**Bash:**
```bash
curl -X PUT http://localhost:8080/sneeze/1 \
  -H "Content-Type: application/json" \
  -d "{\"notes\":\"Updated notes\",\"occurred_at\":\"2025-03-01T10:00:00Z\",\"location\":\"Office\",\"volume\":4}"
```

**PowerShell:**
```powershell
$body = '{"notes":"Updated notes","occurred_at":"2025-03-01T10:00:00Z","location":"Office","volume":4}'
Invoke-RestMethod -Uri http://localhost:8080/sneeze/1 -Method Put -Body $body -ContentType "application/json"
```

### Delete sneeze

**Bash:**
```bash
curl -X DELETE http://localhost:8080/sneeze/1
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri http://localhost:8080/sneeze/1 -Method Delete
```


## File Structure

Architecture for a FastAPI app using [Logto](https://logto.io/) for auth and [SQLModel](https://fastapi.tiangolo.com/tutorial/sql-databases/) for persistence, with a clean domain-driven layout.

### Principles

- **Domain-driven**: Each business area (e.g. sneezes, users) lives in its own package with models, schemas, and optional domain logic.
- **Thin routers**: Route modules only handle HTTP and delegate to services or direct DB access.
- **Shared core**: Auth (Logto), DB session, and config are in a central `core` package and injected via FastAPI dependencies.
- **Layered data models**: Per the [FastAPI SQL tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/#create-multiple-models), use a **table model** (SQLModel, `table=True`) for the database and separate **data models** for create/update/response so the API never accepts or exposes internal fields (e.g. server-generated IDs, secrets).

### Directory layout

```
snzr/
├── main.py                 # FastAPI app, lifespan, router includes
├── core/
│   ├── __init__.py
│   ├── config.py           # Settings (env, Logto endpoint, DB URL)
│   ├── db.py               # create_engine, get_session dependency, create_db_and_tables
│   └── auth.py             # Logto/JWT validation, get_current_user dependency
├── domains/
│   ├── __init__.py
│   ├── sneeze/
│   │   ├── __init__.py
│   │   ├── models.py      # Sneeze (table), SneezeCreate, SneezeUpdate, SneezePublic (data models)
│   │   └── crud.py        # Optional: create_sneeze, get_sneeze, list_sneezes, update_sneeze, delete_sneeze
│   └── user/              # If you model users in-app (e.g. profile)
│       ├── __init__.py
│       └── models.py
├── routers/
│   ├── __init__.py
│   ├── sneezes.py         # POST/GET/PUT or PATCH/DELETE /sneezes, depends on session + current_user
│   └── users.py
├── internal/              # Admin or internal-only routes (optional)
│   └── admin.py
├── requirements.txt
└── README.md
```

### Responsibilities

| Layer | Role |
|-------|------|
| **main.py** | Create app, register routers, run `create_db_and_tables()` on startup (or use lifespan). |
| **core/config.py** | Pydantic `BaseSettings`: `DATABASE_URL`, Logto issuer/audience/app ID for JWT validation. |
| **core/db.py** | SQLModel `engine`, `get_session()` dependency (yield `Session`), `create_db_and_tables(engine)`. |
| **core/auth.py** | Validate Logto-issued JWTs (e.g. via `python-jose` or Logto SDK), dependency `get_current_user` returning user id or a small user object. |
| **domains/\*/models.py** | **Table model**: `class Sneeze(SQLModel, table=True)` with id, user_id, notes, occurred_at, etc. **Data models**: `SneezeCreate`, `SneezeUpdate`, `SneezePublic` (no `table=True`); use inheritance (e.g. `SneezeBase`) to avoid duplication. |
| **domains/\*/crud.py** | Functions that take `Session` and model instances; perform add/commit/refresh, select, update, delete. Keeps DB logic out of routers. |
| **routers/\*.py** | APIRouter with path operations; inject `Session` and `current_user`, parse body as `SneezeCreate`/`SneezeUpdate`, call crud, return `SneezePublic` or list thereof. Use `response_model=SneezePublic` and 201/204/404 where appropriate. |

### Auth (Logto)

- Use Logto as the OIDC provider; the frontend (or client) gets tokens from Logto.
- Backend validates the access token (JWT) on each request: in **core/auth.py**, verify signature and claims using Logto’s JWKS endpoint (or SDK), then expose `get_current_user` as a dependency.
- Protect routes with `Depends(get_current_user)`; use the returned user id when creating or filtering domain entities (e.g. sneezes by `user_id`).

### Persistence (SQLModel)

- One **engine** in **core/db.py** (e.g. SQLite for dev, PostgreSQL for prod via `config.DATABASE_URL`).
- One **session per request** via `get_session()` with `yield`, and `SessionDep = Annotated[Session, Depends(get_session)]`.
- Table models in **domains/\*/models.py**; create tables on startup with `SQLModel.metadata.create_all(engine)`.
- For create: accept `SneezeCreate`, build `Sneeze` (table) with `Sneeze.model_validate(create_model)` and set `user_id` from `get_current_user`; for update use `model_dump(exclude_unset=True)` and `sqlmodel_update` for partial updates.

This layout keeps domains isolated, auth and DB in one place, and aligns with [FastAPI’s SQL tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/) and [Logto](https://logto.io/) for a scalable, maintainable API.
