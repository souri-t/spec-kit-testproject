
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

SETTINGS_FILE = "/workspace/spec-kit-testproject/backend/settings.json"
RESULTS_FILE = "/workspace/spec-kit-testproject/backend/results.json"

class Settings(BaseModel):
    prompt: str
    execution_time: str  # e.g., "09:00"
    api_key: str

def query_ai():
    if not os.path.exists(SETTINGS_FILE):
        with open(RESULTS_FILE, 'w') as f:
            json.dump({"error": "No settings found"}, f, indent=4)
        return {"error": "No settings found"}

    try:
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
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
                model="openai/gpt-4o-mini",
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
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings.dict(), f, indent=4)
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
                return json.load(f)
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
