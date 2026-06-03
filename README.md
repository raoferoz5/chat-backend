# Chat Backend API

A production-ready chat backend built with FastAPI, PostgreSQL, SQLAlchemy, and WebSockets. The application provides secure user authentication, chat room management, real-time messaging, and persistent message storage through a RESTful API and WebSocket connections.

## 🚀 Live Demo

**API Base URL**
https://chat-backend-production-d04b.up.railway.app

**Swagger Documentation**
https://chat-backend-production-d04b.up.railway.app/docs

---

## 📌 Features

### Authentication & Security
- User registration and login
- JWT-based authentication
- Password hashing using bcrypt
- Protected API endpoints

### Chat System
- Create and manage chat rooms
- Send and retrieve messages
- Room-based message organization
- Real-time communication with WebSockets
- Online user tracking

### Data Management
- PostgreSQL database integration
- SQLAlchemy ORM for database operations
- Message history persistence
- Paginated message retrieval

### Deployment
- Docker containerization
- Railway cloud deployment
- Alembic database migrations
- Environment-based configuration

---

## 🛠 Technology Stack

| Category | Technologies |
|-----------|-------------|
| Backend Framework | FastAPI |
| Language | Python 3.12 |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | JWT, OAuth2 |
| Password Security | bcrypt |
| Real-Time Communication | WebSockets |
| Database Migrations | Alembic |
| Containerization | Docker |
| Deployment | Railway |

---

## 🏗 System Architecture

```text
Client Applications
        │
        ▼
    FastAPI API
        │
 ┌──────┴──────┐
 ▼             ▼
REST API   WebSockets
 ▼             ▼
SQLAlchemy  Connection Manager
        │
        ▼
    PostgreSQL
```

---

## 📂 Project Structure

```text
chat-backend/
│
├── app/
│   ├── models/
│   │   ├── user.py
│   │   ├── chat_room.py
│   │   └── message.py
│   │
│   ├── routers/
│   │   ├── user.py
│   │   └── chat.py
│   │
│   ├── database.py
│   ├── config.py
│   └── main.py
│
├── alembic/
├── migrations/
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🗄 Database Design

### Users

| Column | Type |
|----------|--------|
| id | Integer |
| username | String |
| email | String |
| password | String |

### Chat Rooms

| Column | Type |
|----------|--------|
| id | Integer |
| room_name | String |

### Messages

| Column | Type |
|----------|--------|
| id | Integer |
| room_id | Integer |
| sender_id | Integer |
| content | Text |
| created_at | Timestamp |

---

## 🔗 API Endpoints

### Authentication

| Method | Endpoint | Description |
|----------|-----------|-------------|
| POST | /users/register | Register a new user |
| POST | /users/login | Login and receive JWT token |
| GET | /users/me | Get authenticated user profile |

### Chat Rooms

| Method | Endpoint | Description |
|----------|-----------|-------------|
| GET | /chat/rooms | Retrieve all chat rooms |
| POST | /chat/rooms | Create a new chat room |

### Messages

| Method | Endpoint | Description |
|----------|-----------|-------------|
| POST | /chat/messages | Send a message |
| GET | /chat/messages/{room_id} | Retrieve room messages |

### Online Users

| Method | Endpoint | Description |
|----------|-----------|-------------|
| GET | /chat/rooms/{room_id}/online | Get online user count |

---

## ⚙️ Local Installation

### Clone Repository

```bash
git clone https://github.com/raoferoz5/chat-backend.git
cd chat-backend
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

### Run Database Migrations

```bash
alembic upgrade head
```

### Start Application

```bash
uvicorn app.main:app --reload
```

---

## 🐳 Docker

Build image:

```bash
docker build -t chat-backend .
```

Run container:

```bash
docker run -p 8000:8000 chat-backend
```

---

## 📈 Key Backend Concepts Demonstrated

- REST API development
- JWT authentication
- Database schema design
- SQLAlchemy ORM
- WebSocket communication
- Pagination implementation
- Docker containerization
- Database migrations with Alembic
- Production deployment on Railway

---

## 📬 Contact

**Muhammad Sajid**

- GitHub: https://github.com/raoferoz5
- LinkedIn: https://www.linkedin.com/in/muhammad-sajid-softwaredeveloper/
- Email: raoferoz5@gmail.com
