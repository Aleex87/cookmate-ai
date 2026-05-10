import streamlit as st
import httpx
import os


URL_FASTAPI = os.getenv("API_URL", "http://backend:8000")


def page():
    st.title("Welcome to Cookmate")
    st.divider()
    st.header("How does this work?")
    st.markdown(""" 
                In the box below you put in the ingredients you have at home and Cookmate will give you a recipe based on what you have at home.
                """)

    input_ingrediens = st.text_input(
        label="Put in ingredients here",
        placeholder="Example: pasta tomato egg chilli",
    )

    if st.button("Send in"):
        if input_ingrediens == "":
            st.write("You did not put anything in?")
            return

        list_of_input = [
            item.strip()
            for item in input_ingrediens.replace(",", " ").split()
            if item.strip()
        ]

        try:
            res_response = httpx.post(
                f"{URL_FASTAPI}/recipes",
                timeout=180,
                json={"ingredients": list_of_input},
            )
            res_response.raise_for_status()
        except httpx.HTTPError as error:
            st.error(f"Backend request failed: {error}")
            return

        try:
            data_res = res_response.json()
        except ValueError:
            st.error("Backend returned a non-JSON response.")
            st.text(res_response.text)
            return

        recepies = data_res.get("recipes", [])

        for recipe in recepies:
            st.subheader(recipe["title"])

            for step in recipe["steps"]:
                st.write(step)

        # TODO: fix the download button later.
        # st.download_button(label="Download to PDF", data=str, file_name="json.pdf")


if __name__ == "__main__":
    page()
    