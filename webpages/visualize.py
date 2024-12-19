import streamlit as st
# from streamlit import components as html
# import streamlit.components.html as html
import streamlit.components.v1 as components

def visualize_graph():
    st.title("Knowledge Graph")
    
    # Read the HTML content from the file
    with open('network.html', 'r') as file:
        html_content = file.read()

    # Embed the HTML content in the Streamlit app
    components.html(html_content, height=1000, width=1000)
