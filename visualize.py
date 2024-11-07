import streamlit as st
# from streamlit import components as html
# import streamlit.components.html as html
import streamlit.components.v1 as components

def page1():
    st.title("Page 1")
    st.write("This is the content of Page 1.")
    # Read the HTML content from the file
    with open('network.html', 'r') as file:
        html_content = file.read()

    # Embed the HTML content in the Streamlit app
    components.html(html_content, height=1000, width=1000)
