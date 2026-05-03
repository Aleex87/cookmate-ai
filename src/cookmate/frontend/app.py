import streamlit as st
import httpx 


def page():
    st.title("Welcome to cookmaite")
    st.divider()
    st.header("How does this work?")
    st.markdown(""" 
                In the box below you put in the ingrediens you have at home and cookmate will give you a recepic base on what you have at home
                """)
    input_ingrediens = st.text_input(label="Put in ingrediens here")

    

def export():
    pass 

