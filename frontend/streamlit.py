import streamlit as st
import requests
import os


# URL de l'API FastAPI
API_URL = "http://localhost:8000/fruits"

st.title("Fruits list")
st.image(os.path.join(os.getcwd(), "../backend/static", "img.png"), width = 500)
def get_fruits():
    response = requests.get(API_URL)
    fruits = response.json()["data"]
    return fruits

def delete_fruit(id):
    response = requests.delete(API_URL+"/"+id)
    if response.status_code == 200:
        fruit = response.text
        st.session_state.fruit_deleted = fruit
    return response

def edit_fruit(id,new_name):
    print('start')
    update_fruit_request = {
        "id": id,
        "new_name": new_name
      }
    print(update_fruit_request)
    response = requests.put(API_URL,json = update_fruit_request)
    print(response)
    if response.status_code == 200:
        fruit = response.text
        st.session_state.fruit_edited = fruit
    return response

def display_fruits(fruits):
    if fruits:
        for fruit in fruits:
            col1, col2, col3 = st.columns([4, 1, 3])

            with col1:
                st.write(fruit["name"])

            with col2:
                delete_button = st.button(f"Delete", key="delete"+fruit["id"], on_click=delete_fruit, args=(fruit["id"],))

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
                                edit_fruit(fruit["id"], new_name)
                                # After submission, set the editing state to False
                                st.session_state["editing_" + fruit["id"]] = False
                                st.rerun()

    else:
        st.write("Aucun fruit à afficher.")



fruits = get_fruits()
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
            response = requests.post(API_URL, json={"name":new_fruit})
            if response.status_code == 200:
                st.session_state.fruit_added = new_fruit
                st.rerun()
            else:
                st.error("Failed to add fruit")

        else:
            st.warning("Please enter a new fruit")