# Streamlit Docker Deployment Guide

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```
Build and run the container:
```bash
docker build -t fraud-detection-ui .
docker run -p 8501:8501 fraud-detection-ui
```
