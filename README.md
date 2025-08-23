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
-   **Containerization**: Docker + Docker Compose
-   **Auth**: JWT Authentication

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

### API Documentation

📖 You can explore and test the API with Postman:

[👉 Postman API Guide](https://documenter.getpostman.com/view/25520088/2sB3BLjTTi)

---
