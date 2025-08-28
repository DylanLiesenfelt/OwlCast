import requests

def get_data():
    """
    Fetch weather data from the National Weather Service API.
    Returns a list of forecast periods if successful, otherwise None.
    """
    url = 'https://api.weather.gov/gridpoints/MFL/111,77/forecast'
    response = requests.get(url)

    try:
        response.raise_for_status()
        data = response.json()
        data = data['properties']['periods']

        return data

    except requests.exceptions.RequestException as e:
        print(f'Error fetching NWS data: {e}')

        return None

