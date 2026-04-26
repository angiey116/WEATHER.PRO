from flask import request, jsonify
from database import WeatherDatabase
from weather_api import get_weather_observation
from flask import render_template

def register_routes(app):
    @app.get("/")
    def home():
        return render_template("index.html")
    
    @app.get("/ingest")
    def ingest_weather():
        city = request.args.get("city")
        country = request.args.get("country")
        
        if not city or not country:
            return jsonify({"error": "city and country parameters are required"}), 400
        
        observation = get_weather_observation(city, country)
        if observation is None:
            return jsonify({"error": "could not get weather observation from API"}), 404
        
        db = WeatherDatabase(
            dbname="weather_project",
            user="postgres",
            password="cubbies1",
            host="localhost",
            port="5432"
        )
        
        try:
            new_id = db.insert_observation(observation)
            saved_observation = db.get_observation_by_id(new_id)
            
            return jsonify({
                "id": saved_observation[0],
                "city": saved_observation[1],
                "country": saved_observation[2],
                "latitude": saved_observation[3],
                "longitude": saved_observation[4],
                "temperature": saved_observation[5],
                "windspeed": saved_observation[6],
                "elevation": saved_observation[7],
                "observation_time": saved_observation[8],
                "notes": saved_observation[9]
            }), 200
        finally:
            db.close()
    
    @app.get("/observations")
    def get_all_observations():
        db = WeatherDatabase(
            dbname="weather_project",
            user="postgres",
            password="cubbies1",
            host="localhost",
            port="5432"
        )
        
        try:
            observations = db.get_all_observations()
            
            results = []
            for obs in observations:
                results.append({
                    "id": obs[0],
                    "city": obs[1],
                    "country": obs[2],
                    "latitude": obs[3],
                    "longitude": obs[4],
                    "temperature": obs[5],
                    "windspeed": obs[6],
                    "elevation": obs[7],
                    "observation_time": obs[8],
                    "notes": obs[9]
                })
            return jsonify(results), 200
        finally:
            db.close()
    
    @app.get("/observations/<int:observation_id>")
    def get_observation_by_id(observation_id):
        db = WeatherDatabase(
            dbname="weather_project",
            user="postgres",
            password="cubbies1",
            host="localhost",
            port="5432"
        )
        
        try:
            obs = db.get_observation_by_id(observation_id)
            if obs is None:
                return jsonify({"error": "Observation not found"}), 404
            
            return jsonify({
                "id": obs[0],
                "city": obs[1],
                "country": obs[2],
                "latitude": obs[3],
                "longitude": obs[4],
                "temperature": obs[5],
                "windspeed": obs[6],
                "elevation": obs[7],
                "observation_time": obs[8],
                "notes": obs[9]
            }), 200
        finally:
            db.close()
    
    @app.put("/observations/<int:observation_id>")
    def update_observation_notes(observation_id):
        data = request.get_json()
        if not data or "notes" not in data:
            return jsonify({"error": "notes field is required"}), 400
        
        new_notes = data["notes"]
        
        db = WeatherDatabase(
            dbname="weather_project",
            user="postgres",
            password="cubbies1",
            host="localhost",
            port="5432"
        )
        
        try:
            existing = db.get_observation_by_id(observation_id)
            if existing is None:
                return jsonify({"error": "Observation not found"}), 404
            
            updated = db.update_notes_by_id(observation_id, data["notes"])
            
            return jsonify({
                "id": updated[0],
                "notes": updated[1]
            }), 200
        finally:
            db.close()
    
    @app.delete("/observations/<int:observation_id>")
    def delete_observation(observation_id):
        db = WeatherDatabase(
            dbname="weather_project",
            user="postgres",
            password="cubbies1",
            host="localhost",
            port="5432"
        )
        
        try:
            existing = db.get_observation_by_id(observation_id)
            if existing is None:
                return jsonify({"error": "Observation not found"}), 404
            
            db.delete_observation_by_id(observation_id)
            
            return jsonify({
                "deleted": observation_id
            }), 200
        finally:
            db.close()