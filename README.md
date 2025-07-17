# Datadog Training

This repository provides a FastAPI application instrumented with Datadog that performs CRUD operations on a `Person` resource. The data is persisted in a MySQL database and a small front‑end is provided to interact with the API.

## Setup

1. Create a `.env` file with your database credentials. A template is provided in `.env.example`:

```bash
cp .env.example .env
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

Start the application using `uvicorn`:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`. Navigate to `http://localhost:8000` in your browser to use the simple front‑end. API documentation is available at `http://localhost:8000/docs`.
