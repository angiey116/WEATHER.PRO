# WEATHER.PRO

## PROJECT DESCRIPTION
Weather.PRO is a Python Flask API that gets real-time weather data from the Open_Meteo API. It allows users to get, update, and delete weather observations. 

---

## Technologies Used
- Python
- Flask
- PostgreSQL
- Open-Meteo API
- VS Code

---

## Features
- Fetch weather data for cities using an external API
- Store weather observations in a database
- Retrieve all observations
- Retrieve a single observation by ID
- Update notes for an observation
- Delete an observation

---

## Project Structure
- main.py -> fetches weather data and inserts it into the database
- weather_api.py -> handles API calls to Open-Meteo
- databse.py -> manages database connection and CRUD operations
- routes.py -> defined API endpoints
- app.py -> creates and configures the Flask app
- run.py -> runs the Flask server

---

## How to Run
1. In terminal: pip install flask psycopg2 requests
2. Run the server: python run.py
3. Open in Browser at http://127.0.0.1:5000

--

## Routes
1. Get homepage:
http://127.0.0.1:5000/
2. Ingest Weather:
http://127.0.0.1:5000/ingest?city=Chicago&country=US
3. Get all observations:
http://127.0.0.1:5000/observations
4. Get one observation:
http://127.0.0.1:5000/observations/1