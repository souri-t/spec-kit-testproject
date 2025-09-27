
from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
from openai import OpenAI
from datetime import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

app = FastAPI()

import os
from cryptography.fernet import Fernet
import base64

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'settings.json')
RESULTS_FILE = os.path.join(os.path.dirname(__file__), 'results.json')
ENCRYPTION_KEY_FILE = os.path.join(os.path.dirname(__file__), 'encryption.key')

def generate_or_load_key():
    if not os.path.exists(ENCRYPTION_KEY_FILE):
        key = Fernet.generate_key()
        with open(ENCRYPTION_KEY_FILE, 'wb') as f:
            f.write(key)
    with open(ENCRYPTION_KEY_FILE, 'rb') as f:
        return f.read()

def encrypt_api_key(api_key: str, key: bytes) -> str:
    f = Fernet(key)
    encrypted = f.encrypt(api_key.encode())
    return base64.urlsafe_b64encode(encrypted).decode()

def decrypt_api_key(encrypted_api_key: str, key: bytes) -> str:
    f = Fernet(key)
    decoded = base64.urlsafe_b64decode(encrypted_api_key.encode())
    return f.decrypt(decoded).decode()

KEY = generate_or_load_key()

class Settings(BaseModel):
    prompt: str
    execution_time: str  # e.g., "09:00"
    api_key: str
    model: str = "openai/gpt-4o-mini"

def query_ai():
    if not os.path.exists(SETTINGS_FILE):
        with open(RESULTS_FILE, 'w') as f:
            json.dump({"error": "No settings found"}, f, indent=4)
        return {"error": "No settings found"}

    try:
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
        settings['api_key'] = decrypt_api_key(settings['api_key'], KEY)
    except Exception as e:
        error_msg = str(e)
        with open(RESULTS_FILE, 'w') as f:
            json.dump({"error": error_msg}, f, indent=4)
        return {"error": error_msg}

    client = OpenAI(
        api_key=settings['api_key'],
        base_url="https://openrouter.ai/api/v1"
    )

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=settings.get('model', 'openai/gpt-4o-mini'),
                messages=[{"role": "user", "content": settings['prompt']}]
            )
            result = {
                "timestamp": datetime.now().isoformat(),
                "prompt": settings['prompt'],
                "response": response.choices[0].message.content
            }
            try:
                with open(RESULTS_FILE, 'w') as f:
                    json.dump(result, f, indent=4)
            except Exception as save_e:
                return {"error": f"Query succeeded but save failed: {str(save_e)}"}
            return result
        except Exception as e:
            if attempt == max_retries - 1:
                error_msg = f"Failed after {max_retries} attempts: {str(e)}"
                with open(RESULTS_FILE, 'w') as f:
                    json.dump({"error": error_msg}, f, indent=4)
                return {"error": error_msg}
            time.sleep(2 ** attempt)  # Exponential backoff

@app.post("/settings")
def save_settings(settings: Settings):
    try:
        encrypted_key = encrypt_api_key(settings.api_key, KEY)
        save_data = settings.dict()
        save_data['api_key'] = encrypted_key
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(save_data, f, indent=4)
        # Update scheduler if needed
        scheduler = getattr(app.state, 'scheduler', None)
        if scheduler:
            scheduler.remove_all_jobs()
            hour, minute = map(int, settings.execution_time.split(':'))
            scheduler.add_job(
                query_ai,
                CronTrigger(hour=hour, minute=minute),
                id='daily_query'
            )
        return {"status": "saved"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/settings")
def get_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                data['api_key'] = decrypt_api_key(data['api_key'], KEY)
                # Fill defaults if missing
                settings_obj = Settings(**data)
                return settings_obj.dict()
        except Exception as e:
            return {"error": str(e)}
    return {"error": "No settings found"}

@app.get("/result")
def get_result():
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            return {"error": str(e)}
    return {"error": "No result found"}

@app.post("/query")
def trigger_query():
    result = query_ai()
    return result

@app.on_event("startup")
def startup_event():
    app.state.scheduler = BackgroundScheduler()
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
            hour, minute = map(int, settings['execution_time'].split(':'))
            app.state.scheduler.add_job(
                query_ai,
                CronTrigger(hour=hour, minute=minute),
                id='daily_query'
            )
        except Exception as e:
            print(f"Failed to schedule: {e}")
    app.state.scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    if hasattr(app.state, 'scheduler'):
        app.state.scheduler.shutdown()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=50214)
