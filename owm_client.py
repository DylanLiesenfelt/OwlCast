import os
import requests
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv('OWM_API_KEY')

lat = 26.3730
lon = -80.0986
url = f'https://api.openweathermap.org/data/3.0/onecall?lat={26.3730}&lon={-80.0986}&appid={KEY}'

print(url)
try:
    print('trying url')
    response = requests.get(url)
    data = response.json()

    print(response, data)
except requests.ConnectionError as e:
    print(f'ERROR: {e}')