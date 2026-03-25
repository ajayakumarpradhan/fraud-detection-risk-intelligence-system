# Enterprise Deployment Strategy

## 1. Local Hosting
Run FastAPI background server:
`uvicorn api:app --host 0.0.0.0 --port 8000`

## 2. Server Hosting (AWS / Azure)
Ensure ports 8000 and 8501 are exposed to the internet.
`pip install -r requirements.txt`
