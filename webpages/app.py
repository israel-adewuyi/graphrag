import streamlit as st
import requests
import threading
import uvicorn
from main import app
import streamlit_antd_components as sac

from queryllm import process_queries
from visualize import visualize_graph

# Function to run FastAPI in the background
def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000)

# Start FastAPI in a separate thread
threading.Thread(target=run_fastapi, daemon=True).start()

# Sidebar navigation
with st.sidebar.container():
    st.subheader("Navigation Menu")
    menu = sac.menu(
        items=[
            sac.MenuItem("Home"),
            sac.MenuItem("Visualize Knowledge Graph")
        ],
        open_all=True
    )

# select actions
with st.container():
    if menu == "Home":
        process_queries()
    elif menu == "Visualize Knowledge Graph":
        visualize_graph()

st.markdown(
r"""
<img src="https://raw.githubusercontent.com/callummcdougall/computational-thread-art/master/example_images/misc/prereqs.png" width="600">
            
# Highlighted Podcast(s)
<div style="display: flex; justify-content: center; ">
<iframe width="700" height="304" src="https://www.youtube.com/embed/UTuuTTnjxMQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

""", unsafe_allow_html=True)
