# Axe Hack City API

Backend API for a text-based game, built with FastAPI + SQLAlchemy.

## Getting Started

This repository is **backend-only**. It provides API endpoints and game logic, but no frontend/UI code.

### Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/) (recommended)
- Docker + Docker Compose (optional, for full local stack)

---

### Option A: Run locally with Python (fastest setup)

Use this path when you just want to run the API quickly.

1. **Clone and enter the repo**
   ```bash
   git clone <your-repo-url>
   cd axe-hack-city-api
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Create environment file**
   ```bash
   cp .env.example .env
   ```
   If `.env.example` is not present, create `.env` manually with at least:
   ```env
   DATABASE_URL=sqlite:///axe_hack_city/app.db
   ENVIRONMENT=development
   MINIO_ENDPOINT=localhost:9000
   MINIO_ACCESS_KEY=minioadmin
   MINIO_SECRET_KEY=minioadmin
   MINIO_BUCKET=axe-hack-city-assets
   MINIO_SECURE=false
   ```

4. **Start the API**
   ```bash
   make dev
   ```
   Or directly:
   ```bash
   poetry run uvicorn axe_hack_city.main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Verify it is running**
   - API root/docs: `http://localhost:8000/docs`

> On startup, the app initializes database tables automatically via `initialize_database()`.
> The SQLite file is generated at runtime (for local/dev) and should never be committed.

---

### Option B: Run with Docker Compose (full dev stack)

Use this path when you want the full service stack: API + Postgres + Redis + MinIO.

1. **Start core services**
   ```bash
   docker compose up --build
   ```

2. **(Optional) include pgAdmin UI**
   ```bash
   docker compose --profile admin up --build
   ```

3. **Service endpoints**
   - API: `http://localhost:8000`
   - API docs: `http://localhost:8000/docs`
   - Postgres: `localhost:5432`
   - Redis: `localhost:6379`
   - MinIO API: `http://localhost:9000`
   - MinIO Console: `http://localhost:9001`
   - pgAdmin (admin profile): `http://localhost:5050`

4. **Stop services**
   ```bash
   docker compose down
   ```

---

### Common local workflows

- Run tests:
  ```bash
  poetry run pytest
  ```
- Format code:
  ```bash
  make format
  ```
- Lint code:
  ```bash
  make lint
  ```

## Frontend Options (there is no frontend in this repo)

You have several good choices depending on your goals:

1. **Flask + Jinja templates (quickest server-rendered UI)**
   - Good for: admin tools, simple prototype screens, rapid iteration.
   - Pros: minimal JS, easy to host with backend.
   - Cons: less interactive UX for game loops.

2. **React (recommended for game client UX)**
   - Good for: interactive HUDs, inventory panels, mission/state updates, websockets later.
   - Pros: rich component ecosystem, scalable architecture.
   - Cons: separate app/build pipeline.

3. **Next.js (React framework)**
   - Good for: React UI plus routing, API proxying, and optional SSR.
   - Pros: production-ready conventions out of the box.
   - Cons: slightly more framework complexity.

4. **Lightweight HTML/JS client first, upgrade later**
   - Good for: validating API/gameplay quickly before committing to a full frontend stack.
   - Pros: lowest initial effort.
   - Cons: harder to scale as UI complexity grows.

### Practical recommendation

- If your immediate goal is to build a real player-facing interface, start with **React** (or **Next.js** if you want routing/SSR conventions).
- If your immediate goal is just testing and internal tooling, a **Flask/Jinja** UI is fine as a temporary bridge.

---

## Database Bootstrap (Canonical Path)

The canonical schema source of truth is the SQLAlchemy ORM models in `axe_hack_city/models/`.

On API startup, `axe_hack_city/main.py` calls `initialize_database()` from
`axe_hack_city/database/bootstrap.py`, which:

1. Loads all model modules so their tables are registered on shared metadata.
2. Creates tables with `Base.metadata.create_all(bind=engine)`.

### What to use
- Use `initialize_database()` for local/bootstrap table creation.
- Keep schema definitions in SQLAlchemy models.
- If/when migrations are introduced, they should become the only schema evolution path.

### What not to use
- Do **not** use legacy raw-SQL bootstrap scripts. The previous
  `axe_hack_city/database/create_tables.py` path was removed to avoid schema drift.
- Do **not** commit generated database artifacts (for example `app.db`); let startup/bootstrap create tables from models.

---

## Interconnections Between Files

This section outlines how different files within the project interact to handle API requests and manage data flow. Each component has a specific role in maintaining a clean architecture and ensuring separation of concerns.

### 1. **Routers (`routers/`)**
- **Purpose**: Define API endpoints and handle incoming requests.
- **Interconnections**:
  - **Imports the relevant controller** for handling business logic (e.g., `from ..controllers.<entity>_controller import <Entity>Controller`).
  - **Imports request and response schemas** for data validation (e.g., `from ..schemas.<entity>_schema import <Entity>CreateSchema, <Entity>Schema`).

### 2. **Controllers (`controllers/`)**
- **Purpose**: Serve as intermediaries between routers and repositories, containing business logic.
- **Interconnections**:
  - **Imports the repository** for database operations (e.g., `from ..database.sqlalchemy_repository import SQLAlchemyRepository`).
  - **Imports the model** representing the database entity (e.g., `from ..models.<entity>_model import <Entity>`).

### 3. **Repositories (`database/`)**
- **Purpose**: Handle all database interactions using SQLAlchemy, abstracting the database layer.
- **Interconnections**:
  - **Does not import routers or controllers**, ensuring it remains independent.
  - **Works with models** that represent the structure of database entities (e.g., `from ..models.<entity>_model import <Entity>`).

### 4. **Models (`models/`)**
- **Purpose**: Define the structure of database entities using SQLAlchemy ORM.
- **Interconnections**:
  - **Should not import any other modules**; it exists solely to define data structures.

### 5. **Schemas (`schemas/`)**
- **Purpose**: Define Pydantic models for request and response validation.
- **Interconnections**:
  - **Does not need to import routers or controllers**, operating independently to provide validation functionality.

### Example Flow for API Requests

1. **Client sends a request** (e.g., POST, GET) to an endpoint defined in the router.
2. **Router validates the request** against the schema and calls the corresponding controller method.
3. **Controller processes the request**, applying business logic and invoking methods from the repository.
4. **Repository interacts with the database** using the model to perform the required operations.
5. **Repository returns the result** to the controller, which formats the response.
6. **Router sends the response** back to the client, completing the request-response cycle.

### Benefits of this Structure
- **Separation of Concerns**: Each component has a clear responsibility, making the code easier to manage and extend.
- **Testability**: Isolated components can be tested independently, improving the overall quality of the application.
- **Scalability**: New features and endpoints can be added without significant modifications to existing code.

---

## Additional container suggestions for MMORPG-scale growth
- **Nginx or Traefik** for TLS termination, routing, and load balancing across multiple API replicas.
- **Celery worker + Celery beat** for async/background tasks (combat ticks, world events, notifications).
- **Prometheus + Grafana** for metrics and dashboards.
- **Loki + Promtail** (or ELK/OpenSearch) for centralized logs.
- **Keycloak** (or Authentik) for robust account/session identity management.
- **RabbitMQ or NATS** if game event throughput outgrows Redis pub/sub.
