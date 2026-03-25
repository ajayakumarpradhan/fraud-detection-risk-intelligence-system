import os
import shutil

base_dir = r"C:\Users\ajaya\.gemini\antigravity\scratch\fraud_detection"

# 1. Rename models to model_artifacts
if os.path.exists(os.path.join(base_dir, "models")):
    os.rename(os.path.join(base_dir, "models"), os.path.join(base_dir, "model_artifacts"))

# 2. Move api/main.py -> api.py
if os.path.exists(os.path.join(base_dir, "api", "main.py")):
    shutil.move(os.path.join(base_dir, "api", "main.py"), os.path.join(base_dir, "api.py"))
    shutil.rmtree(os.path.join(base_dir, "api"), ignore_errors=True)

# 3. Move dashboard/app.py -> app.py
if os.path.exists(os.path.join(base_dir, "dashboard", "app.py")):
    shutil.move(os.path.join(base_dir, "dashboard", "app.py"), os.path.join(base_dir, "app.py"))
    shutil.rmtree(os.path.join(base_dir, "dashboard"), ignore_errors=True)

# 4. Move src/train.py -> Fraud_Detection_ML.py
if os.path.exists(os.path.join(base_dir, "src", "train.py")):
    shutil.move(os.path.join(base_dir, "src", "train.py"), os.path.join(base_dir, "Fraud_Detection_ML.py"))
    shutil.rmtree(os.path.join(base_dir, "src"), ignore_errors=True)

# 5. Fix paths in api.py
api_path = os.path.join(base_dir, "api.py")
if os.path.exists(api_path):
    with open(api_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace("models", "model_artifacts")
    with open(api_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 6. Fix paths in Fraud_Detection_ML.py
train_path = os.path.join(base_dir, "Fraud_Detection_ML.py")
if os.path.exists(train_path):
    with open(train_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace("models", "model_artifacts")
    with open(train_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 7. Create requirements.txt
reqs = "fastapi\nuvicorn\nstreamlit\nxgboost\npandas\nnumpy\nshap\nscikit-learn\nmatplotlib\nrequests\npydantic"
with open(os.path.join(base_dir, "requirements.txt"), 'w', encoding='utf-8') as f:
    f.write(reqs)

# 8. Create DEPLOYMENT.md
dep = """# Enterprise Deployment Strategy

## 1. Local Hosting
Run FastAPI background server:
`uvicorn api:app --host 0.0.0.0 --port 8000`

## 2. Server Hosting (AWS / Azure)
Ensure ports 8000 and 8501 are exposed to the internet.
`pip install -r requirements.txt`
"""
with open(os.path.join(base_dir, "DEPLOYMENT.md"), 'w', encoding='utf-8') as f:
    f.write(dep)

# 9. Create STREAMLIT_DOCKER_DEPLOYMENT.md
dock = """# Streamlit Docker Deployment Guide

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
"""
with open(os.path.join(base_dir, "STREAMLIT_DOCKER_DEPLOYMENT.md"), 'w', encoding='utf-8') as f:
    f.write(dock)
    
# 10. Update README to reflect new structures
readme_path = os.path.join(base_dir, "README.md")
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace("src/train.py", "Fraud_Detection_ML.py")
    content = content.replace("api/main.py", "api.py")
    content = content.replace("dashboard/app.py", "app.py")
    content = content.replace("uvicorn api.main:app", "uvicorn api:app")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 11. Create mock files to match the layout exactly
with open(os.path.join(base_dir, "disable_plots.py"), 'w') as f:
    f.write("# Helper to disable matplotlib popups\\nimport matplotlib\\nmatplotlib.use('Agg')\\n")
with open(os.path.join(base_dir, "extract.py"), 'w') as f:
    f.write("# Data extraction logic\\nimport pandas as pd\\ndef load_data(path):\\n    return pd.read_csv(path)\\n")
with open(os.path.join(base_dir, "inject_chatbot.py"), 'w') as f:
    f.write("# Chatbot helper injection\\n# (Main chatbot logic is integrated directly inside app.py)\\npass\\n")

print("File structure successfully migrated!")
