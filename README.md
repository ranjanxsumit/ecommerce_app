# HROne Backend Intern Task: E-Commerce API

This project is a simple e-commerce backend application built with FastAPI and MongoDB as per the hiring task specification.

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
    MONGO_URI=your_mongodb_connection_string
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the Application

Run the application using Uvicorn from the project's root directory:
```bash
python -m uvicorn main:app --reload