from dataclasses import dataclass
import psycopg2


@dataclass
class WeatherObservation:
    city: str
    country: str
    latitude: float
    longitude: float
    temperature: float
    windspeed: float
    elevation: float
    observation_time: str


class WeatherDatabase:
    def __init__(self, dbname, user, password, host="localhost", port="5432"):
        self.connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()
        print("Connected to database successfully.")

    def insert_observation(self, observation):
        query = """
        INSERT INTO weather_observations
        (city, country, latitude, longitude, temperature, windspeed, elevation, observation_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """

        values = (
            observation.city,
            observation.country,
            observation.latitude,
            observation.longitude,
            observation.temperature,
            observation.windspeed,
            observation.elevation,
            observation.observation_time
        )

        self.cursor.execute(query, values)
        new_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return new_id

    def get_all_observations(self):
        query = "SELECT * FROM weather_observations;"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_observation_by_id(self, observation_id):
        query = "SELECT * FROM weather_observations WHERE id = %s;"
        self.cursor.execute(query, (observation_id,))
        return self.cursor.fetchone()

    def update_notes_by_id(self, observation_id, notes):
        query = """
        UPDATE weather_observations
        SET notes = %s
        WHERE id = %s
        RETURNING id, notes;
        """
        self.cursor.execute(query, (notes, observation_id))
        self.connection.commit()
        return self.cursor.fetchone()

    def delete_observation_by_id(self, observation_id):
        query = "DELETE FROM weather_observations WHERE id = %s;"
        self.cursor.execute(query, (observation_id,))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
        print("Database connection closed.")