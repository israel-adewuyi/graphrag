import streamlit as st
import requests
import threading
import uvicorn
from main import app

from queryllm import process_queries
from visualize import page1

# Function to run FastAPI in the background
def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000)

# Start FastAPI in a separate thread
threading.Thread(target=run_fastapi, daemon=True).start()


# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Navigation", ["Ask a question", "Visualize Graph",])

# Display the selected page
if page == "Ask a question":
    process_queries()
elif page == "Visualize Graph":
    page1()
