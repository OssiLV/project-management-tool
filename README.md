# Project Management Tool API

## 📝 1. Project Description

A project management system following the **Kanban/Scrum** model. Users can:

-   Create projects and invite members.
-   Create boards (Kanban boards).
-   Create lists (To Do, In Progress, Done).
-   Create tasks (assign to members, add labels, attach files).
-   Comment and discuss within tasks.
-   Receive notifications for important events (assigned to a task, new comments, etc.).

## ⚙️ 2. Tech Stack

-   **Backend**: Python (FastAPI)
-   **Database**: MariaDB (one schema per service)
-   **ORM**: SQLAlchemy
-   **Migration**: Alembic
-   **Containerization**: Docker + Docker Compose
-   **Auth**: JWT (JSON Web Token) – stateless authentication between microservices.
-   **Load Balancing / Reverse Proxy**: Nginx
-   **Testing**: coming soon...
-   **CI/CD**: coming soon...
-   **Monitoring/Logging**: coming soon...

## 🚀 How to start project

### Create your `.env` file

```bash
cp .env.example .env
```

Open the `.env` file and **add your own values** (database, secrets, etc.).

### Run docker

```bash
docker compose up -d
```

## API Documentation

📖 Explore and test the API with `Swagger UI`:

> Port default: **8080**

-   http://localhost:8080/auth_service/docs
-   http://localhost:8080/project_service/docs
-   coming soon...

📬 You can explore and test the API with `Postman`:

-   [Postman API Guide](https://documenter.getpostman.com/view/25520088/2sB3BLjTTi)

## 🗄️ Database Migration Guide

When you **add a new field to a model** (inside `app/models/...py`), you need to create an Alembic migration to update the schema.

### Create a new migration version

1. Find the container ID or name of the service you want to migrate.

    Example for `auth_service`:

    ```bash
    docker ps
    ```

    ```bash
    CONTAINER ID   IMAGE                                   COMMAND            NAMES
    72d0d214f153   project-management-system-auth_service  "./entrypoint.sh" project-management-system-auth_service-1
    ```

2. Run the migration command inside the container:

    ```bash
    docker exec -it project-management-system-auth_service-1 alembic revision --autogenerate -m "Your message"
    ```

    Alembic will generate a new migration file under `migrations/versions/`.

### Apply the migration (upgrade)

After the migration file is created, upgrade the database:

```bash
docker exec -it project-management-system-auth_service-1 alembic upgrade head
```

### Restart the service

Once the database has been updated, restart the container service to load the changes:

```bash
docker restart project-management-system-auth_service-1
```

---
