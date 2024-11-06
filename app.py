import streamlit as st
import requests

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

            # Display the results
            st.subheader("Response:")
            # for result in results:
            st.write(results)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    else:
        st.warning("Please enter a query.")
