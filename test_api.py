import time
import requests

url_predict = "http://127.0.0.1:8000/predict"
url_explain = "http://127.0.0.1:8000/explain"

payload = {
    "step": 3,
    "type": "TRANSFER",
    "amount": 100000.0,
    "oldbalanceOrg": 100000.0,
    "newbalanceOrig": 0.0,
    "oldbalanceDest": 0.0,
    "newbalanceDest": 0.0
}

try:
    print("Testing /predict...")
    r1 = requests.post(url_predict, json=payload)
    print(r1.json())
    
    print("\nTesting /explain...")
    r2 = requests.post(url_explain, json=payload)
    print(r2.json())
except Exception as e:
    print(f"Error connecting to API: {e}")
