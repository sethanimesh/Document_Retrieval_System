# Document Retrieval System

## Overview

This project implements a document retrieval system using **FastAPI** for the API, **FAISS** for efficient vector-based document search, and an SQL database (SQLite) for tracking user requests. The system allows users to query documents and retrieve results based on similarity, with a rate-limiting feature that restricts each user to 5 API requests. If the user exceeds the limit, an HTTP 429 status code is returned.

## Features

- **Document Retrieval**: Documents are stored as vector embeddings using FAISS, enabling efficient similarity-based searches.
- **Rate Limiting**: Each user can make up to 5 API requests. If a user exceeds this limit, further requests return HTTP 429 (Too Many Requests).
- **User Tracking**: Each user's API requests are tracked in an SQL database, where the frequency of their requests is incremented for each call.
- **FastAPI Framework**: FastAPI is used to handle HTTP requests and serve the API.
- **SQL Database**: A SQL database (SQLite) is used to track the number of API calls made by each user.

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- pip (Python package installer)

### Clone the Repository

```bash
git clone https://github.com/sethanimesh/21BBS0053_ML.git
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

The dependencies include:
- **FastAPI**: For building the API.
- **Uvicorn**: For running the FastAPI application.
- **SQLAlchemy**: For managing database interactions.
- **FAISS**: For similarity search using vector embeddings.
- **Sentence-Transformers**: For encoding documents into vector embeddings.

### Set Up the Database

The application uses SQLite for simplicity. The database schema will automatically be created when the application is run for the first time.

## Running the Application

To start the FastAPI server, run the following command:

```bash
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## API Endpoints

### 1. `/search` (POST)

This endpoint allows users to search for similar documents.

#### Request:
- **Method**: `POST`
- **Body** (JSON):
  - `user_id` (str): A unique identifier for the user.
  - `text` (str): The query text.
  - `top_k` (int, optional): The number of top results to return. Default is 5.
  - `threshold` (float, optional): The similarity score threshold. Default is 0.5.

#### Example Request:

```json
{
  "user_id": "user123",
  "text": "Jio AI-Cloud Welcome Offer",
  "top_k": 3,
  "threshold": 10.0
}
```

#### Response:
- **200 OK**: Returns the top documents based on the query.
- **404 Not Found**: If no documents match the query.
- **429 Too Many Requests**: If the user has exceeded 5 API calls.

#### Example Response:

```json
{
  "results": [
    {
      "document": "Jio AI-Cloud Welcome Offer: Reliance has announced the Jio AI-Cloud Welcome Offer to be launched this Diwali...",
      "distance": 2.3
    },
    {
      "document": "Reliance is focusing on AI-driven services through Jio Phone and Jio Home IoT services...",
      "distance": 4.5
    }
  ]
}
```

### 2. `/health` (GET)

A simple health check to verify if the API is running.

#### Example Response:

```json
{
  "status": "API is active and running!"
}
```

## Database

The system uses **SQLite** to store user request data. The `users_details` table keeps track of how many times a user has made a request.

### Table Schema:

| Field         | Type    | Description                              |
|---------------|---------|------------------------------------------|
| `user_id`     | String  | The unique identifier for the user.       |
| `request_count` | Integer | The number of API requests made by the user. |

- If a user exceeds 5 requests, an HTTP 429 status is returned for additional requests.

## FAISS for Document Search

FAISS is used to store and retrieve documents based on their vector embeddings. Documents are encoded using **Sentence-Transformers** to generate vector embeddings, and FAISS performs a similarity search using the L2 (Euclidean) distance.

## Project Structure

```
.
├── main.py                   # FastAPI application code
├── faiss_embedding.py         # FAISS setup for document embeddings
├── models.py                 # SQLAlchemy models
├── database.py               # Database session management
├── requirements.txt           # Python dependencies
└── README.md                 # Project documentation
```

### `faiss_embedding.py`
This file is responsible for initializing FAISS, encoding documents using Sentence-Transformers, and adding them to the FAISS index for efficient similarity search.

### `main.py`
This file contains the FastAPI application logic, including the `/search` and `/health` endpoints, and the logic for rate limiting based on user requests.

### `models.py`
Defines the SQLAlchemy models, including the `User` table that tracks user requests.

### `database.py`
Handles the SQLite database connection and session management using SQLAlchemy.

## Future Enhancements

- **Support for Multiple Document Types**: Add support for document types other than plain text, such as PDFs or Word documents.
- **Advanced Caching**: Implement Redis or other caching mechanisms to cache search results for faster retrieval.
- **Authentication**: Add user authentication and API key validation for added security.
- **Pagination**: Implement pagination for large search results.
- **Search Index Optimization**: Explore advanced FAISS index types (e.g., `IVF`, `HNSW`) for faster searches on large datasets.

## License

This project is licensed under the MIT License.
