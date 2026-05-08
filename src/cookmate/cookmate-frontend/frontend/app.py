import streamlit as st
import httpx 
import os
import json 


URL_FASTAPI = os.getenv("URL_FASTAPI", "http://localhost:8000")




def page():
    st.title("Welcome to cookmate")
    st.divider()
    st.header("How does this work?")
    st.markdown(""" 
                In the box below you put in the ingrediens you have at home and cookmate will give you a recepic base on what you have at home
                """)
    input_ingrediens = st.text_input(label="Put in ingridens here")
    list_of_input = [item.strip()
                    for item in input_ingrediens.split(",")]

    if st.button("Send in"):
        if input_ingrediens == "":
            st.write("you did not put anything in?")
       
    res_response = httpx.post(f"{URL_FASTAPI}/recipes", timeout=180, json={"ingredients": list_of_input})
    

    data_res = json.loads(res_response.text)
    recepies = data_res.get("recipes", [])
    
    for recipe in recepies:
        st.subheader(recipe["title"]) 

        for step in recipe["steps"]:
            st.write(step)
   

    st.download_button(label="Download to PDF", data=str, file_name="json.pdf")  #steamlit docs on how to use download button i8n combo wioth LLM  

if __name__ == "__main__":
    page()
