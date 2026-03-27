# Chat Application API Documentation

## Base URL

```
http://127.0.0.1:8000/users/
```

---

## 1. User Registration API

### Endpoint

```
POST /users/
```

### Description

Creates a new user account.

### Request Body

```json
{
  "username": "testuser",
  "password": "123456",
  "first_name": "John",
  "last_name": "Doe",
  "email": "test@gmail.com",
  "phone_number": "9876543210",
  "country_code": 1
}
```

### Success Response (201)

```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "testuser",
    "first_name": "John",
    "last_name": "Doe",
    "email": "test@gmail.com",
    "phone_number": "9876543210",
    "country_code": 1
  }
}
```

### Error Response (400)

```json
{
  "success": false,
  "error": {
    "email": ["Enter a valid email address."]
  }
}
```

---

## 2. User Login API

### Endpoint

```
POST /login/
```

### Description

Authenticates user using **email or phone number + password** and returns JWT tokens.

---

### Request Body (Email Login)

```json
{
  "email": "test@gmail.com",
  "password": "123456"
}
```

### Request Body (Phone Login)

```json
{
  "phone_number": "9876543210",
  "password": "123456"
}
```

---

### Success Response (200)

```json
{
  "access": "your_access_token",
  "refresh": "your_refresh_token",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@gmail.com"
  }
}
```

---

### Error Response (400)

```json
{
  "non_field_errors": [
    "Invalid credentials"
  ]
}
```

---

## Authentication Usage

For protected APIs, include token in header:

```
Authorization: Bearer <access_token>
```

---

## Notes

* Password is securely hashed.
* Email and phone should be unique (recommended).
* JWT tokens are used for authentication.

---
