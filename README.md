# Fruity App 🍏

A simple web application to manage fruits using FastAPI, MongoDB, Streamlit, Docker, and AWS EC2. 

You can access the frontend [here](http://ec2-51-21-245-77.eu-north-1.compute.amazonaws.com:8501/)

## Features
- Add, delete, edit fruits via a Streamlit frontend
- FastAPI backend with MongoDB database
- Dockerized deployment
- Hosted on an AWS EC2 instance

## Deployment

1. Clone the repository on your EC2 instance.
2. Run the containers:

```
docker compose up --build -d
```
3. Access the app:
   
Frontend (Streamlit): http://ec2-51-21-245-77.eu-north-1.compute.amazonaws.com:8501/

Backend (FastAPI docs): http://ec2-51-21-245-77.eu-north-1.compute.amazonaws.com:8000/docs

## Tech Stack
- Frontend: Streamlit
- Backend: FastAPI
- Database: MongoDB
- Deployment: Docker + AWS EC2

