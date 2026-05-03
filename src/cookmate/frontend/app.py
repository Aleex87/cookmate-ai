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

    if st.button("Send in") and input_ingrediens == "":
        st.write("you did not put anything in?")
    
    res_response = httpx.post(f"")
    data_res = res_response.json()

    st.markdown(input_ingrediens)
    st.markdown(data_res.get())
    st.markdown(data_res.get())

def export():
    pass 


if __name__ == "__main__":
    page()
