import streamlit as st
import requests
import threading
import uvicorn
from main import app  # Import FastAPI app

# Function to run FastAPI in the background
def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000)

# Start FastAPI in a separate thread
threading.Thread(target=run_fastapi, daemon=True).start()

# Define the FastAPI endpoint URL
FASTAPI_URL = "http://127.0.0.1:8000/query_similarity"

# Streamlit app title
st.title("Graphrag Query Interface")

# Input form for the query
query = st.text_input("Enter your query:")

if st.button("Submit"):
    if query:
        # Prepare the request payload
        payload = {"query": query}

        # Make a POST request to the FastAPI endpoint
        response = requests.post(FASTAPI_URL, json=payload)

        if response.status_code == 200:
            # Parse the response JSON
            results = response.json().get("results", [])
            st.subheader("Response:")
            st.write(results)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    else:
        st.warning("Please enter a query.")
