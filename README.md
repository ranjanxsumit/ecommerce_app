# Backend Task: E-Commerce API

# 🛒 E-Commerce API Project

This project is a simplified backend API for an e-commerce platform inspired by Flipkart/Amazon. It allows users to manage product listings and order placements. The APIs are built using FastAPI with MongoDB Atlas as the backend database.

---

## 📦 Features

### 1. Create Product API
- **Endpoint**: `/products`
- **Method**: `POST`
- **Description**: Adds a new product to the inventory.
- **Response**: 
  - Status Code: `201 Created`

---

### 2. List Products API
- **Endpoint**: `/products`
- **Method**: `GET`
- **Description**: Fetches product listings with optional filters.
- **Query Parameters** (all optional):
  - `name`: Partial/regex search on product name
  - `size`: Filter by size (e.g., `large`)
  - `limit`: Number of products to return
  - `offset`: Number of products to skip (pagination, sorted by `_id`)
- **Response**: 
  - Status Code: `200 OK`

---

### 3. Create Order API
- **Endpoint**: `/orders`
- **Method**: `POST`
- **Description**: Creates a new order for a product.
- **Response**: 
  - Status Code: `201 Created`

---

### 4. List Orders API
- **Endpoint**: `/orders/<user_id>`
- **Method**: `GET`
- **Description**: Retrieves orders placed by a specific user.
- **Query Parameters** (all optional):
  - `limit`: Number of orders to return
  - `offset`: Number of orders to skip (pagination, sorted by `_id`)
- **Response**: 
  - Status Code: `200 OK`

---

## 🧪 Tech Stack

- **Language**: Python `3.10+`
- **Framework**: FastAPI
- **Database**: MongoDB Atlas (M0 Free Tier)
- **ORM/Connector**: Pymongo or Motor

---

## Project Structure

- `main.py`: The entry point of the FastAPI application.
- `database.py`: Handles MongoDB connection.
- `config.py`: Manages environment variables.
- `models/`: Contains Pydantic data models for request and response validation.
- `crud/`: Contains functions for all database operations (Create, Read, Update, Delete).
- `routers/`: Defines the API endpoints and connects them to the CRUD functions.
- `requirements.txt`: Lists all Python dependencies.
- `.env`: (You must create this file) Stores environment variables like the database connection string.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd ecommerce_app
    ```

2.  **Create `.env` file:**
    Create a file named `.env` in the project root and add your MongoDB connection string:
    ```
    MONGODB_URI=your_mongodb_connection_string
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the Application

Run the application using Uvicorn from the project's root directory:
```bash
python -m uvicorn main:app --reload
