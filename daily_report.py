import nws_client
from datetime import datetime

"""
Generate a daily weather report for FAU Boca Campus using data from the National Weather Service.
"""

def get_date_info():
    """
    Get the current date and format it for the report header.
    Returns a string with the formatted date.
    """
    current_date = datetime.today().strftime('%A %B %d %Y')

    return f'Today is {current_date}.\nHeres the forecast for FAU Boca Campus!\n'

def make_day_forecast(data):
    """
    Returns the daytime weather forecast.
    """
    return f'\nFor the Morning into the Afternoon you can expect:\n {data['detailedForecast']}'

def make_night_forecast(data):
    """
    Returns the nighttime weather forecast.
    """
    return f'\n\nFor this Evening you can expect:\n {data['detailedForecast']}'

def make_report():
    """
    Generate and print the full daily weather report.
    """
    date_info = get_date_info()
    data = nws_client.get_data()
    
    if data:
        day_forecast = data[0]
        night_forecast = data[1]
    else:
        print('ERROR: FAILED TO GET NWS DATA')
        
    report = f'{date_info} {make_day_forecast(day_forecast)} {make_night_forecast(night_forecast)}'

    return report
