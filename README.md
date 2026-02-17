## Dockerized Development Stack

This project now supports a multi-container setup for local virtualization with Docker Compose.

### Included services
- **api**: FastAPI backend (`axe_hack_city.main:app`)
- **postgres**: Primary relational database for concurrent multiplayer workloads
- **minio**: S3-compatible object storage for assets/HUD media
- **minio-init**: Creates the default MinIO bucket automatically
- **redis**: In-memory cache/pub-sub layer for session state and chat fanout
- **pgadmin** (optional profile): Postgres admin UI

### Quick start
1. Build and run core stack:
   ```bash
   docker compose up --build
   ```
2. Run with pgAdmin UI:
   ```bash
   docker compose --profile admin up --build
   ```

### Service endpoints
- API: `http://localhost:8000`
- MinIO API: `http://localhost:9000`
- MinIO Console: `http://localhost:9001`
- Redis: `localhost:6379`
- Postgres: `localhost:5432`
- pgAdmin (profile `admin`): `http://localhost:5050`

### Environment variables
Set these in `.env` (or rely on docker-compose defaults):
- `DATABASE_URL`
- `ENVIRONMENT`
- `MINIO_ENDPOINT`
- `MINIO_ACCESS_KEY`
- `MINIO_SECRET_KEY`
- `MINIO_BUCKET`
- `MINIO_SECURE`

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
