# Real-Time Chat Application

## Overview

This project is a **scalable chat application backend** built using Django and Django REST Framework. It provides APIs for user authentication, user discovery, and chat functionality including conversations and messaging.

The system is designed to evolve into a **real-time messaging platform (like WhatsApp)** using WebSockets.

---

## Tech Stack

### Backend

* Python
* Django
* Django REST Framework (DRF)

### Database

* PostgreSQL

### Authentication

* JWT (JSON Web Tokens)

### Frontend

* React.js (integrated)

---

## Features Implemented

### 1. User Management

* User Registration API
* User Login API (Email / Phone + Password)
* JWT-based Authentication

---

### 2. User Discovery

* Get all users
* Search users by:

  * Username
  * Email
  * Phone number

---

### 3. Chat System (Core)

* Create Conversation (1-to-1 chat)
* Prevent duplicate conversations
* Send Messages
* Store chat history

---

## API Summary

### User APIs

* `POST /users/users/` → Register user
* `POST /users/login/` → Login user
* `GET /users/users/` → Get/Search users

---

### Chat APIs

* `POST /chat/conversations/` → Create/Get conversation
* `GET /chat/conversations/` → List user conversations
* `POST /chat/messages/` → Send message
* `GET /chat/messages/` → Get messages

---

## Project Architecture

### Users App

Handles:

* Authentication
* User data
* User search

### Chat App

Handles:

* Conversations (chat rooms)
* Messages
* Chat logic

---

## Data Model Overview

### Conversation

* Represents a chat between users
* Supports multiple participants (future group chat)

### Message

* Linked to a conversation
* Stores sender, content, timestamp, read status

---

## Vision

The goal of this project is to build a **production-ready real-time chat system** with:

* Live messaging using WebSockets (Django Channels)
* Typing indicators
* Read receipts
* Group chats
* Media sharing
* Scalable architecture for high user load

---

## Future Enhancements

* Real-time communication (Django Channels)
* Online/offline user status
* Message read/unread tracking
* Push notifications
* File/image sharing
* Deployment on cloud (AWS/Docker)

---

## Getting Started

### 1. Clone the repository

```bash
git clone <repo-url>
cd project
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup PostgreSQL database

Update `settings.py` with your DB credentials.

---

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 5. Run server

```bash
python manage.py runserver
```

---

## Authentication Usage

Add JWT token in headers:

```bash
Authorization: Bearer <access_token>
```

---

## Conclusion

This project follows **clean architecture and scalable design principles**, making it suitable for evolving into a **full-featured real-time chat platform**.

---
