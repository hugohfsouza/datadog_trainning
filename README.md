# Datadog Training

This repository provides a simple FastAPI application that performs CRUD operations on a `Person` resource. The data is stored in memory.

## Setup

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

Run the application using `uvicorn`:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000` with automatically generated docs at `http://localhost:8000/docs`.
