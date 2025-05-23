import os
import requests
import streamlit as st

API_BASE_URL = "http://backend:8000"

st.title("Grocery Product Search")
st.image(os.path.join(os.getcwd(), "static", "img.png"), width=500)



# Inputs
search_term = st.text_input("Enter product name (e.g. tomato, apple, broccoli)")
supermarket = st.selectbox("Select supermarket", options=["amazon"])

# Define helper functions outside the if block

def query_already_searched(search_term: str, supermarket: str) -> bool:
    try:
        response = requests.get(f"{API_BASE_URL}/queries/")
        response.raise_for_status()
        queries = response.json().get("data", [])
        return any(q["search_term"] == search_term and q["supermarket"] == supermarket for q in queries)
    except requests.RequestException as e:
        st.error(f"Error checking query: {e}")
        return False

def fetch_products_from_db(search_term: str, supermarket: str):
    try:
        response = requests.get(
            f"{API_BASE_URL}/products/product",
            params={"tags": search_term, "supermarket": supermarket}
        )
        response.raise_for_status()
        return response.json().get("data", [])
    except requests.RequestException as e:
        st.error(f"Error fetching products from DB: {e}")
        return []

def trigger_search(search_term: str, supermarket: str):
    try:
        payload = {
            "search_term": search_term,
            "supermarket": supermarket
        }
        response = requests.post(
            f"{API_BASE_URL}/search/search",
            json=payload  # Send JSON body
        )
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.RequestException as e:
        st.error(f"Error triggering search: {e}")
        return []

# Button logic
if st.button("Search"):
    if search_term and supermarket:
        if query_already_searched(search_term, supermarket):
            st.info("Query already exists — loading from database")
            products = fetch_products_from_db(search_term, supermarket)
        else:
            st.info("New query — calling external API")
            products = trigger_search(search_term, supermarket)

        # Display products 3 per row
        if products:
            st.subheader(f"Results for '{search_term}' from {supermarket}")
            for i in range(0, len(products), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(products):
                        product = products[i + j]
                        with cols[j]:
                            image_url = product.get("image_url")
                            if image_url:
                                st.image(image_url, width=150)
                            st.markdown(f"**{product.get('name', 'Unnamed')}**")
                            st.write(f"Price: {product.get('price', 'N/A')}")

        else:
            st.warning("No products found.")
    else:
        st.warning("Please enter a product name and select a supermarket.")
