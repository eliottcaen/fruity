import os
import streamlit as st
from class_fruit import Fruit

# URL of the FastAPI backend
# API_URL = "http://localhost:8000/fruits"  # Running locally
API_URL = "http://backend:8000/fruits"


fruit_api = Fruit(API_URL)

st.title("Fruits List")

# Display an image at the top of the page
st.image(os.path.join(os.getcwd(), "static", "img.png"), width=500)


# Display Fruits in a free-floating style with Edit and Delete buttons
def display_fruits(fruits):
    if fruits:
        for fruit in fruits:
            # Create a row with columns for each piece of fruit info and buttons
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])  # Adjust column sizes as needed
            with col1:
                st.write(f"**{fruit['name']}**")
            with col2:
                st.write(f"Price: {fruit.get('price', 'N/A')}")
            with col3:
                st.write(f"Supermarket: {fruit.get('supermarket', 'N/A')}")
            with col4:
                # Add Edit and Delete buttons next to each fruit
                edit_button = st.button(f"Edit {fruit['name']}", key=f"edit_{fruit['id']}")
                delete_button = st.button(f"Delete {fruit['name']}", key=f"delete_{fruit['id']}")

                if edit_button:
                    # Trigger editing for this fruit
                    st.session_state["editing_fruit_id"] = fruit['id']
                    st.session_state["editing_fruit"] = fruit
                    st.rerun()  # Rerun to display the editing form

                if delete_button:
                    response = fruit_api.delete_fruit(fruit['id'])
                    print('ici', response)
                    if response["status"] == "ok":
                        st.session_state["fruit_deleted"] = fruit['name']
                        st.rerun()
                    else:
                        st.error("Failed to delete fruit")

    else:
        st.write("No fruits available.")


# Edit Fruit Form
def edit_fruit_form(fruit):
    st.subheader("Edit Fruit Details")
    with st.form(key="edit_fruit_form"):
        new_name = st.text_input("Fruit Name", value=fruit['name'])
        new_price = st.number_input("Price", min_value=0.0, value=fruit.get('price', 0.0))
        new_supermarket = st.text_input("Supermarket", value=fruit.get('supermarket', ''))

        submit_button = st.form_submit_button(label="Save Changes")
        if submit_button:
            if new_name and new_price >= 0:
                updated_fruit = {"new_name": new_name, "new_price": new_price, "new_supermarket": new_supermarket}
                response = fruit_api.edit_fruit(fruit['id'], updated_fruit)
                if response["status"] == "ok":
                    # Close the editing panel after successful update
                    st.session_state["editing_fruit_id"] = None  # Reset the editing session
                    st.session_state["editing_fruit"] = None  # Reset the fruit data being edited
                    st.session_state["fruit_updated"] = new_name
                    st.rerun()  # Refresh the page to reflect the update
                else:
                    st.error("Failed to update fruit")
            else:
                st.warning("Please fill in all fields correctly.")


# If an editing session exists, show the form
if "editing_fruit_id" in st.session_state and st.session_state["editing_fruit_id"]:
    fruit_to_edit = st.session_state["editing_fruit"]
    edit_fruit_form(fruit_to_edit)

# Display Fruits List
fruits = fruit_api.get_fruits()
display_fruits(fruits)

# Feedback after actions
if "fruit_deleted" in st.session_state:
    st.success(f"{st.session_state['fruit_deleted']} was deleted successfully.")
    del st.session_state["fruit_deleted"]

if "fruit_updated" in st.session_state:
    st.success(f"{st.session_state['fruit_updated']} was updated successfully.")
    del st.session_state["fruit_updated"]

# Add a new fruit form
with st.form(key="add_a_fruit"):
    st.header("Add a New Fruit")
    new_fruit_name = st.text_input("Enter the name of a new fruit")
    new_fruit_price = st.number_input("Enter the price", min_value=0.0, value=0.0)
    new_fruit_supermarket = st.text_input("Enter the supermarket name")

    add_fruit_button = st.form_submit_button("Add Fruit")
    if add_fruit_button:
        if new_fruit_name and new_fruit_price >= 0:
            response = fruit_api.add_fruit(new_fruit_name, new_fruit_price, new_fruit_supermarket)
            if response["status"] == "ok":
                st.session_state["fruit_added"] = new_fruit_name
                st.rerun()
            else:
                st.error("Failed to add fruit.")
        else:
            st.warning("Please fill in all fields correctly.")
