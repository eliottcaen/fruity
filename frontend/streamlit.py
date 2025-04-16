import streamlit as st
import os
from class_fruit import Fruit


# URL de l'API FastAPI
API_URL = "http://localhost:8000/fruits"
fruit_api = Fruit(API_URL)

st.title("Fruits list")
st.image(os.path.join(os.getcwd(), "../backend/static", "img.png"), width = 500)


def display_fruits(fruits):
    if fruits:
        for fruit in fruits:
            col1, col2, col3 = st.columns([4, 1, 3])

            with col1:
                st.write(fruit["name"])

            with col2:
                delete_button = st.button(f"Delete", key="delete"+fruit["id"], on_click=fruit_api.delete_fruit, args=(fruit["id"],))

            with col3:
                # Check if we are currently editing this fruit
                if "editing_" + fruit["id"] not in st.session_state:
                    st.session_state["editing_" + fruit["id"]] = False

                edit_button = st.button(f"Edit", key="edit" + fruit["id"])

                if edit_button:
                    # Set the editing state to True when the Edit button is clicked
                    st.session_state["editing_" + fruit["id"]] = True

                if st.session_state["editing_" + fruit["id"]]:
                    # Once in editing mode, show the form
                    with st.form(key="edit a fruit"):
                        new_name = st.text_input("Enter the new fruit name", key="input" + fruit["id"])
                        submit_button = st.form_submit_button(label="Submit")

                        # If the form is submitted, update the fruit's name
                        if submit_button:
                            new_name = st.session_state.get("input" + fruit["id"])
                            if new_name:
                                print(new_name)
                                # Call the function to edit the fruit
                                fruit_api.edit_fruit(fruit["id"], new_name)
                                # After submission, set the editing state to False
                                st.session_state["editing_" + fruit["id"]] = False
                                st.rerun()
                            else:
                                st.warning("Please write a new name")

    else:
        st.write("Aucun fruit à afficher.")



fruits = fruit_api.get_fruits()
display_fruits(fruits)

if "fruit_deleted" in st.session_state:
    st.success(f"{st.session_state.fruit_deleted} was deleted successfully")
    del st.session_state["fruit_deleted"]

if "fruit_added" in st.session_state:
    st.success(f"{st.session_state.fruit_added} was added successfully")
    del st.session_state["fruit_added"]

# Add a fruit
with st.form(key="add_a_fruit"):
    st.header("Add a fruit")
    if 'new_fruit' not in st.session_state:
        st.session_state.new_fruit = ""

    new_fruit = st.text_input("Enter the name of a fruit", value=st.session_state.new_fruit)

    submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        if new_fruit != "":
            response = fruit_api.add_fruit(new_fruit)
            if response["status"] == "ok":
                st.session_state.fruit_added = new_fruit
                st.success(f"Fruit {new_fruit} added successfully!")
                st.rerun()
            else:
                st.error("Failed to add fruit")
        else:
            st.warning("Please enter a new fruit")