import requests
from datetime import date

def get_data():
    """
    Fetch weather data from the National Weather Service API.
    Returns a list of forecast periods if successful, otherwise None.
    """
    url = 'https://api.weather.gov/gridpoints/MFL/111,77/forecast'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        data = data['properties']['periods']

        return data

    else:
        print('Could not reach NWS servers')

        return None

