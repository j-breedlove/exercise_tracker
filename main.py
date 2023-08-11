import datetime as dt
import os

import requests
from dotenv import load_dotenv

# Loading environment variables from .env file
load_dotenv(".env")

# Constants
GENDER = os.getenv("GENDER")
WEIGHT_KG = float(os.getenv("WEIGHT_KG"))
HEIGHT_CM = float(os.getenv("HEIGHT_CM"))
AGE = int(os.getenv("AGE"))
NUTRITIONIX_ENDPOINT = os.getenv("NUTRITIONIX_ENDPOINT")
NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY")
NUTRITIONIX_API_ID = os.getenv("NUTRITIONIX_API_ID")
SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")
SHEETY_AUTH = os.getenv("SHEETY_AUTH")
BASIC_AUTH_USER = os.getenv("BASIC_AUTH_USER")
BASIC_AUTH_PASS = os.getenv("BASIC_AUTH_PASS")


def get_exercise_data(exercise_text):
    """Fetches exercise data from the Nutritionix API."""
    nutritionix_headers = {
        "x-app-key": NUTRITIONIX_API_KEY,
        "x-app-id": NUTRITIONIX_API_ID,
        "x-remote-user-id": "0",
        "Content-Type": "application/json"
    }
    data = {
        "query": exercise_text,
        "gender": GENDER,
        "weight_kg": WEIGHT_KG,
        "height_cm": HEIGHT_CM,
        "age": AGE
    }
    response = requests.post(url=NUTRITIONIX_ENDPOINT, json=data, headers=nutritionix_headers)
    return response.json()


def record_exercise_to_sheety(exercise_text):
    """Records exercise data to the Sheety endpoint."""
    today_date = dt.datetime.now().strftime("%d/%m/%Y")
    now_time = dt.datetime.now().strftime("%X")

    # Prompting user for duration and calories burned
    duration = input(f"How long did you do the {exercise_text} for (in minutes)? ")
    calories = input(f"How many calories did you burn doing the {exercise_text}? ")

    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise_text.title(),
            "duration": duration,
            "calories": calories
        }
    }
    sheety_response = requests.post(url=SHEETY_ENDPOINT, json=sheet_inputs)
    print(sheety_response.json())


def main():
    exercise_text = input("Tell me which exercises you did: ").lower()
    record_exercise_to_sheety(exercise_text)


if __name__ == "__main__":
    main()
