

import streamlit as st
import requests
import json
import os

BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:50214')

def get_settings():
    try:
        response = requests.get(f"{BACKEND_URL}/settings")
        return response.json()
    except Exception as e:
        st.error(f"Error fetching settings: {e}")
        return None

def save_settings(settings):
    try:
        response = requests.post(f"{BACKEND_URL}/settings", json=settings)
        return response.json()
    except Exception as e:
        st.error(f"Error saving settings: {e}")
        return None

def get_result():
    try:
        response = requests.get(f"{BACKEND_URL}/result")
        return response.json()
    except Exception as e:
        st.error(f"Error fetching result: {e}")
        return None

tab1, tab2 = st.tabs(["Settings", "Results"])

with tab1:
    st.subheader("AI Query Scheduler Settings")
    settings = get_settings()

    if settings and "error" not in settings:
        prompt = st.text_area("Prompt", value=settings.get("prompt", ""), height=200)
        execution_time = st.text_input("Execution Time (HH:MM)", value=settings.get("execution_time", "09:00"))
        api_key = st.text_input("Open Router API Key", value=settings.get("api_key", ""), type="password")
        model = st.text_input("OpenRouter Model", value=settings.get("model", "openai/gpt-4o-mini"))
    else:
        prompt = st.text_area("Prompt", height=200)
        execution_time = st.text_input("Execution Time (HH:MM)", "09:00")
        api_key = st.text_input("Open Router API Key", type="password")
        model = st.text_input("OpenRouter Model", "openai/gpt-4o-mini")

    if st.button("Save Settings"):
        new_settings = {
            "prompt": prompt,
            "execution_time": execution_time,
            "api_key": api_key,
            "model": model
        }
        result = save_settings(new_settings)
        if result and "status" in result:
            st.success("Settings saved successfully!")
            st.rerun()
        else:
            st.error("Failed to save settings.")

with tab2:
    st.subheader("Latest AI Result")
    result = get_result()
    if result and "error" not in result:
        st.write("**Timestamp:**", result.get("timestamp", "N/A"))
        st.write("**Prompt:**", result.get("prompt", "N/A"))
        st.markdown("**Response:**")
        st.write(result.get("response", "N/A"))
    elif result:
        st.error(result.get("error", "Unknown error"))
    else:
        st.warning("No result available. Please set up settings and wait for the next scheduled run or trigger manually.")

if st.button("Trigger Query Now"):
    try:
        response = requests.post(f"{BACKEND_URL}/query")
        query_result = response.json()
        if "error" not in query_result:
            st.success("Query triggered successfully!")
            st.rerun()
        else:
            st.error(f"Query failed: {query_result['error']}")
    except Exception as e:
        st.error(f"Error triggering query: {e}")

