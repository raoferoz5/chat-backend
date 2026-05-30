# Chat Backend

A scalable, containerized asynchronous chat application backend built using modern cloud-native standards. This repository contains the complete RESTful API and WebSocket engine driving real-time multi-room messaging.

---

## 🚀 Tech Stack

- **Framework:** FastAPI (Python 3.12)
- **Database:** PostgreSQL 16
- **ORM:** SQLAlchemy (Async Engine)
- **Security:** JWT Authentication & bcrypt password hashing
- **Real-Time:** WebSockets for instant message delivery
- **DevOps:** Docker & Docker Compose for orchestration

---

## ✨ Features

- 👤 **User Management:** Secure user registration and login endpoints.
- 🔒 **JWT Authentication:** Stateful security with token-based access control.
- 💬 **Real-Time Chat:** Persistent WebSocket connections enabling low-latency chatting.
- 📁 **Room Architecture:** Dynamic chat room creation and multi-room separation.
- 📜 **Data Integrity:** Efficient retrieval of message history with optimized pagination.
- 📦 **Containerized Dev Environment:** Zero-config local spinning using multi-container orchestrations.

---

## 🏗️ Architecture Layout

The application isolates computational logic from data layers through a modular router pattern, utilizing an independent asynchronous worker context specifically for low-latency socket pipelines.

```text
chat-backend/
├── app/
│   ├── models/          # SQLAlchemy Database Schemas
│   ├── routers/         # HTTP Endpoints & WebSocket Handlers
│   ├── database.py      # Synchronous Engine Context
│   ├── database_async.py# Asynchronous Engine for WebSockets
│   └── main.py          # Application Core Entrypoint
├── Dockerfile           # Multi-stage optimized application build
├── docker-compose.yml   # Multi-service network orchestrator
└── requirements.txt     # Locked production dependencies