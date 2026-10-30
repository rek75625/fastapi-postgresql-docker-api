# FastAPI + PostgreSQL Docker Starter

A production-ready template for running a **FastAPI** application with a **PostgreSQL** database, completely containerized using **Docker** and **Docker Compose**.

---

## 🛠️ Tech Stack
* **Backend:** FastAPI (Python 3.11+)
* **Database:** PostgreSQL 15
* **Containerization:** Docker & Docker Compose
* **ORM/Migration (Optional):** SQLAlchemy / Alembic

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have the following installed on your machine:
* [Docker Desktop](https://docker.com)
* [Git](https://git-scm.com)

### 2. Environment Setup
Create a `.env` file in the root directory of your project to store database credentials and configurations:

```env
# PostgreSQL Configurations
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=app_db
POSTGRES_PORT=5432
POSTGRES_HOST=db

# FastAPI Configurations
PROJECT_NAME="FastAPI App"
DATABASE_URL=postgresql://postgres:your_secure_password@db:5432/app_db
```

### 3. Spin Up the Containers
Run the following command to build and launch the application and database in the background:

```bash
docker compose up -d --build
```

The services will initialize on these ports:
* 🌐 **FastAPI Server:** `http://localhost:8000`
* 📑 **Interactive API Docs (Swagger UI):** `http://localhost:8000/docs`
* 📊 **PostgreSQL Database:** `localhost:5432`

---

## 📂 Project Structure
```text
├── app/
│   ├── main.py          # FastAPI application entrypoint
│   ├── config.py        # Environment variables & settings
│   ├── database.py      # SQLAlchemy engine and session setup
│   ├── models.py        # Database models
│   └── schemas.py       # Pydantic validation schemas
├── .env                 # Local environment secrets (Git ignored)
├── .env.example         # Template for environment variables
├── Dockerfile           # FastAPI container blueprint
├── docker-compose.yml   # Multi-container orchestration config
└── requirements.txt     # Python dependencies
```

---

## ⚙️ Docker Configuration Breakdown

### `Dockerfile` (App Service)
```dockerfile
FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### `docker-compose.yml`
```yaml
version: '3.8'

services:
  web:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./app:/code/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    ports:
      - "5432:5432"
    env_file:
      - .env
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d app_db"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

---

## 🛠️ Useful Management Commands

| Action | Command |
| :--- | :--- |
| **Stop all services** | `docker compose down` |
| **View real-time logs** | `docker compose logs -f` |
| **View specific service logs** | `docker compose logs -f web` |
| **Access PostgreSQL CLI (psql)** | `docker compose exec db psql -U postgres -d app_db` |
| **Wipe database & volumes** | `docker compose down -v` |

---

## 🔒 Security Note
* Never commit your actual `.env` file to version control systems like GitHub. 
* Change default passwords (`your_secure_password`) before deploying code to production environments.
