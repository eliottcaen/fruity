# Fruity App 🍏

**Fruity** is a personal full-stack project that fetches food product data from the **Amazon product API**, and displays it with prices and images in a simple app.

This project is meant to practice:

- 🔁 Calling external APIs (Amazon food products)
- 🗄️ Storing and querying product data in MongoDB
- ⚙️ Building a backend with FastAPI
- 🎨 Creating a frontend with Streamlit
- 🚢 Deploying everything with Docker Compose on AWS EC2

You can access the frontend [here](http://ec2-13-61-0-9.eu-north-1.compute.amazonaws.com:8501/)

## 🔁 How It Works

When a user searches for a product:

1. The backend checks **MongoDB** to see if the product has been searched before.
2. If found → it returns the **stored data**.
3. If not, it:
   - Calls the **Amazon API** to fetch product info (price, image, etc.)
   - **Stores** the result in MongoDB
   - Returns the data to the frontend.

The frontend (Streamlit) displays the product info using the API response.

## Tech Stack
- Frontend: Streamlit
- Backend: FastAPI
- Database: MongoDB
- Deployment: Docker + AWS EC2

