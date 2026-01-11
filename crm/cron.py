import os
from datetime import datetime
import requests

LOG_FILE = "/c/Temp/crm_heartbeat_log.txt"

def log_crm_heartbeat():
    # Ensure log directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    message = f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')} CRM is alive"
    
    # Optional: check GraphQL endpoint
    try:
        response = requests.post("http://localhost:8000/graphql", json={"query": "{ hello }"})
        if response.status_code == 200:
            message += " | GraphQL endpoint OK"
        else:
            message += f" | GraphQL returned {response.status_code}"
    except Exception as e:
        message += f" | GraphQL check failed: {str(e)}"

    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")
