import os
import requests
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv('TOMORROW_API_KEY')

url = "https://api.tomorrow.io/v4/weather/forecast?location=26.3730,-80.0986&units=imperial"

headers = {
    "accept": "application/json",
    "accept-encoding": "deflate, gzip, br",
    "apikey": KEY
}

def get_current_weather():
    try:
        response = requests.get(url, headers=headers)
        print(response.status_code)
        
        response.raise_for_status()
        data = response.json()

        weather_code = data["timelines"]["minutely"][4]["values"]["weatherCode"]

        return weather_code
    
    except Exception as e:
        print(f'TOMORROW.IO ERROR: {e}')
        return None

print(get_current_weather())