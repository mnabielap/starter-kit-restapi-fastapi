# 🚀 Starter Kit REST API - FastAPI

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Enabled-336791.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?style=for-the-badge&logo=docker&logoColor=white)

A high-performance, production-ready RESTful API starter kit built with **Python (FastAPI)**, **SQLAlchemy**, and **Pydantic**. 

## ✨ Features

-   **⚡ FastAPI**: One of the fastest Python frameworks available.
-   **🗄️ SQLAlchemy ORM**: Asynchronous-ready ORM supporting **SQLite** (Dev) and **PostgreSQL** (Prod).
-   **🔐 Authentication**: Secure JWT (JSON Web Token) Auth (Login, Register, Refresh, Logout).
-   **🛡️ Security**: Password hashing (Bcrypt), Rate Limiting (SlowAPI), CORS, and Helmet-like headers.
-   **📝 Validation**: Pydantic models for strict Request/Response schema validation.
-   **✈️ Migrations**: Database version control using **Alembic**.
-   **🐳 Docker Ready**: Full containerization support with persistent volumes.
-   **🧪 Custom API Tester**: Built-in Python scripts to test endpoints without Postman.

---

## 🛠️ Project Structure

```text
starter-kit-restapi-fastapi/
├── alembic/                # Database migrations
├── api_tests/              # 🧪 Custom API testing scripts
├── app/
│   ├── api/                # Route handlers (Controllers)
│   ├── core/               # Config & Security
│   ├── crud/               # Database Queries (Services)
│   ├── db/                 # DB Connection & Init
│   ├── models/             # SQLAlchemy Tables
│   ├── schemas/            # Pydantic Schemas (Validation)
│   ├── utils/              # Helper functions
│   └── main.py             # App Entrypoint
├── .env.example            # Environment variables template
├── entrypoint.sh           # Docker entry script
└── requirements.txt        # Python dependencies
```

---

## 🚀 Getting Started (Local Development)

We recommend running the project locally first for development and debugging.

### 1. Prerequisites
*   Python 3.11 or higher
*   Git

### 2. Setup Environment
Clone the repo and install dependencies:

```bash
# Clone the repository
git clone <your-repo-url>
cd starter-kit-restapi-fastapi

# Create a virtual environment (Recommended)
python -m venv env

# Activate environment
# Windows:
.\env\Scripts\activate
# Mac/Linux:
source env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Variables
Copy the example environment file:

```bash
cp .env.example .env
```
Open `.env` and verify the settings. By default, it uses **SQLite** (`sqlite:///./sql_app.db`), which requires no extra setup.

### 4. Initialize Database
Run migrations and create the initial Admin user:

```bash
# Apply database migrations
alembic upgrade head

# Create initial Admin user (admin@example.com / password123)
python -c "from app.db.session import SessionLocal; from app.db.init_db import init_db; init_db(SessionLocal())"
```

### 5. Run the Server
```bash
uvicorn app.main:app --reload --port 3000
```
The API is now running at `http://localhost:3000`.
*   **Swagger UI:** [http://localhost:3000/docs](http://localhost:3000/docs)
*   **ReDoc:** [http://localhost:3000/redoc](http://localhost:3000/redoc)

---

## 🐳 Running with Docker (Production/Full Stack)

If you prefer containerization or want to use **PostgreSQL**, follow these manual steps. We separate the Database and the App into two containers communicating via a custom network.

### 1. Create Network & Volumes
This ensures the DB and App can talk to each other, and data persists even if containers are deleted.

```bash
# Create Network
docker network create restapi_fastapi_network

# Create Volumes (Persist Data)
docker volume create restapi_fastapi_db_volume
docker volume create restapi_fastapi_media_volume
```

### 2. Run PostgreSQL Container
Start the database first.

```bash
docker run -d \
  --name restapi-fastapi-postgres \
  --network restapi_fastapi_network \
  -v restapi_fastapi_db_volume:/var/lib/postgresql/data \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgrespassword \
  -e POSTGRES_DB=restapi_db \
  postgres:15-alpine
```

### 3. Setup Docker Environment
Create a `.env.docker` file in your root directory (or ensure it exists) with the following content:

```properties
PORT=3000
# Note the host is the container name: 'restapi-fastapi-postgres'
DATABASE_URL=postgresql://postgres:postgrespassword@restapi-fastapi-postgres:5432/restapi_db
JWT_SECRET=super_secret_jwt_key_for_docker
ENVIRONMENT=production
```

### 4. Build & Run App Container
Build the image and run it, linking it to the network and volumes.

```bash
# Build the image
docker build -t restapi-fastapi-app .

# Run the container
docker run -d -p 5005:3000 \
  --env-file .env.docker \
  --network restapi_fastapi_network \
  -v restapi_fastapi_media_volume:/app/media \
  --name restapi-fastapi-container \
  restapi-fastapi-app
```

The API is now accessible at **[http://localhost:5005](http://localhost:5005)**.

---

## 📦 Docker Management Cheat Sheet

Useful commands for managing your containers.

| Action | Command |
| :--- | :--- |
| **View Logs** | `docker logs -f restapi-fastapi-container` |
| **Stop App** | `docker stop restapi-fastapi-container` |
| **Start App** | `docker start restapi-fastapi-container` |
| **Remove App** | `docker rm restapi-fastapi-container` |
| **List Volumes** | `docker volume ls` |
| **⚠️ Delete Volume** | `docker volume rm restapi_fastapi_db_volume` *(Deletes all DB data!)* |

---

## 🧪 API Testing (No Postman Required)

This project includes a built-in automated testing suite in the `api_tests/` folder. It automatically handles token management (`secrets.json`) so you don't need to copy-paste tokens manually.

**How to use:**
1.  Ensure the server is running (Local: port 3000 or Docker: port 5005 - *Update `utils.py` base URL if using Docker*).
2.  Run the scripts using Python.

**Step 1: Login as Admin (Run this first!)**
This saves the Access Token to `api_tests/secrets.json`.
```bash
python api_tests/auth_login.py
```

**Step 2: Run User Operations**
Create, List, Update, or Delete users.
```bash
python api_tests/users_create.py
python api_tests/users_get_all.py
```

**Step 3: Test Auth Features**
```bash
python api_tests/auth_refresh_tokens.py
python api_tests/auth_logout.py
```

Check the `api_tests/*.json` files for the detailed output of each request!

---

## 📄 License

[MIT](LICENSE)