import os
import requests
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv('TOMORROW_API_KEY')

lat = 26.3730
lon = -80.0986
url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat},{lon}&units=imperial&apikey={KEY}"



headers = {
    "accept": "application/json",
    "accept-encoding": "deflate, gzip, br"
}

def get_current_weather():
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        status = data['data']['values']['weatherCode']
        
        return status
    except Exception as e:
        print(f'ERROR: {e}')

