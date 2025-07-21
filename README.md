# Advanced E-commerce REST API

This project is a full-featured Django REST Framework-based e-commerce backend. It supports:

- JWT-based authentication (registration, login, profile management)
- Product and category management (admin-only CRUD)
- Order system with stock handling
- Redis caching for performance
- Filtering and pagination for product listing
- Real-time order status updates via WebSocket using Django Channels

---

## Features

- User Registration, Login (JWT Authentication)
- Profile View and Update
- Product and Category Models
- Admin CRUD for Products and Categories
- Add to Cart and Place Orders
- Order Status Management (Pending → Shipped → Delivered)
- User Order History
- Redis Caching for Product/Category Listing
- Filtering and Pagination
- Real-time Notifications using WebSockets and Django Channels

---

## Technologies Used

- Django
- Django REST Framework
- Django Channels
- SimpleJWT
- Redis
- PostgreSQL / SQLite (default)
- WebSockets
- Django Filter

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/omkargarad78/Ecommerce_REST.git
cd ecommerce_api
```

### 2. Create a Virtual Environment
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows

```


### 3. Install Dependencies

```bash
pip install -r requirements.txt
```



### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate

```

## Running the Project

### 1. Run Redis Server
Ensure Redis is installed and running:
```bash
redis-server
```

### 2. Start Django Development Server
Ensure Redis is installed and running:
```bash
python manage.py runserver

```


# E-commerce API – Endpoint Overview

This is a structured overview of available API endpoints for an e-commerce backend built using Django REST Framework (DRF) with JWT authentication.

---

## 🔐 Authentication

| Method | Endpoint                        | Description             |
|--------|----------------------------------|-------------------------|
| POST   | `/api/users/register/`          | Register a new user     |
| POST   | `/api/users/login/`             | Login to get JWT tokens |
| POST   | `/api/users/token/refresh/`     | Refresh access token    |

---

## 👤 User Profile

| Method | Endpoint                    | Description           |
|--------|------------------------------|-----------------------|
| GET    | `/api/users/profile/`       | Get user profile      |
| PUT    | `/api/users/profile/`       | Update profile        |

---

## 🛍️ Products & Categories

| Method | Endpoint                        | Description                            |
|--------|----------------------------------|----------------------------------------|
| GET    | `/api/products/`               | List all products (supports filters)   |
| GET    | `/api/categories/`             | List all categories                    |
| POST   | `/api/products/`               | Create new product (Admin only)        |
| POST   | `/api/categories/`             | Create new category (Admin only)       |

---

## 🛒 Orders

| Method | Endpoint                                      | Description                        |
|--------|------------------------------------------------|------------------------------------|
| POST   | `/api/orders/place/`                          | Place an order with cart items     |
| GET    | `/api/orders/my-orders/`                      | View user's order history          |
| GET    | `/api/orders/my-orders/<id>/`                 | View a specific order              |
| PATCH  | `/api/orders/<id>/update-status/`             | Update order status (Admin only)   |

---

## Notes

- All **protected routes** require a valid JWT token (`Authorization: Bearer <token>`).
- Admin-only routes can only be accessed by users with `is_staff` or `is_superuser` permissions.
- Product listing supports query params like:  



