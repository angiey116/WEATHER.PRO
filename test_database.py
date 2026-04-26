from database import WeatherDatabase
from weather_api import get_weather_observation


def run_tests():
    db = WeatherDatabase(
        dbname="weather_project",
        user="postgres",
        password="cubbies1",
        host="localhost",
        port="5432"
    )

    observation = get_weather_observation("Chicago", "US")

    if observation is None:
        print("Could not get observation from API.")
        db.close()
        return

    print("\nWeather object from API:")
    print(observation)

    new_id = db.insert_observation(observation)
    print("\nInserted new observation with ID:", new_id)

    all_observations = db.get_all_observations()
    print("\nAll observations:")
    for obs in all_observations:
        print(obs)

    one_observation = db.get_observation_by_id(new_id)
    print("\nObservation by ID:")
    print(one_observation)

    db.update_notes_by_id(new_id, "Perfect Weather")
    updated_observation = db.get_observation_by_id(new_id)
    print("\nUpdated observation:")
    print(updated_observation)

    #db.delete_observation_by_id(new_id)
    #deleted_observation = db.get_observation_by_id(new_id)
    #print("\nAfter delete:")
    #print(deleted_observation)

    db.close()


if __name__ == "__main__":
    run_tests()