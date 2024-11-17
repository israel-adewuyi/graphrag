import requests
import streamlit as st


def process_queries():
    # Define the FastAPI endpoint URL
    FASTAPI_URL = "http://127.0.0.1:8000/query_similarity"

    # Streamlit app title
    st.title("The Palantir")

    # Input form for the query
    query = st.chat_input("Enter your query:")

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

    # if st.button("Submit"):
    #     if query:
    #         # Prepare the request payload
    #         payload = {"query": query}

    #         # Make a POST request to the FastAPI endpoint
    #         response = requests.post(FASTAPI_URL, json=payload)

    #         if response.status_code == 200:
    #             # Parse the response JSON
    #             results = response.json().get("results", [])
    #             st.subheader("Response:")
    #             st.write(results)
    #         else:
    #             st.error(f"Error: {response.status_code} - {response.text}")
    #     else:
    #         st.warning("Please enter a query.")