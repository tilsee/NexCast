import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy as np
import openmeteo_requests
import requests_cache
from retry_requests import retry
from io import BytesIO
from PIL import Image


def get_weather():
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)


    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 49.861,
        "longitude": 8.6532,
        "current": ["temperature_2m", "precipitation"],
        "minutely_15": ["temperature_2m", "precipitation"],
        "hourly": ["temperature_2m", "precipitation"],
        "timezone": "Europe/Berlin",
        "forecast_days": 3,
        "models": "best_match"
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]


    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s"),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["precipitation"] = hourly_precipitation
    hourly_dataframe = pd.DataFrame(data = hourly_data)
    return hourly_dataframe

def get_next_24h_weather_data():
    hourly_dataframe = get_weather()  # Ensure this returns a DataFrame.
    hourly_dataframe['date'] = pd.to_datetime(hourly_dataframe['date'])
    current_time = pd.Timestamp.now().floor('H')
    mask = (hourly_dataframe['date'] >= current_time) & (hourly_dataframe['date'] < current_time + pd.Timedelta(hours=24))
    return hourly_dataframe.loc[mask]

def customize_plot(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', which='both', left=False, labelleft=False, right=False, labelright=False)
    ax.xaxis.set_major_formatter(DateFormatter('%H'))

def annotate_max_values(ax, data, column, color, max_value, xytext_offset):
    if not data.empty and pd.notna(max_value):
        max_date = data['date'][data[column] == max_value].iloc[0]
        ax.annotate(f'{str(round(max_value,2))}', xy=(max_date, max_value), xytext=xytext_offset, 
                    textcoords='offset points', ha='center', color=color)

def plot_weather():
    frame_width, frame_height = (480, 150)
    next_24h_data = get_next_24h_weather_data()

    if next_24h_data.empty:
        return "No data available for the next 24 hours.", None, None

    fig, ax1 = plt.subplots(figsize=(frame_width/124, frame_height/124), dpi=124)
    customize_plot(ax1)

    ax1.bar(next_24h_data['date'], next_24h_data['precipitation'], color='black', width=0.03)
    ax2 = ax1.twinx()
    ax2.plot(next_24h_data['date'], next_24h_data['temperature_2m'], color='grey')
    customize_plot(ax2)

    max_precipitation_value = next_24h_data['precipitation'].max()
    max_temperature_value = next_24h_data['temperature_2m'].max()

    annotate_max_values(ax1, next_24h_data, 'precipitation', 'black', max_precipitation_value, (-10, 10))
    annotate_max_values(ax2, next_24h_data, 'temperature_2m', 'grey', max_temperature_value, (10, 10))

    plt.tight_layout()
    plt.subplots_adjust(left=0.1, bottom=0.136, right=0.926, top=0.99)

    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    plot_image_pil = Image.open(buf).resize((frame_width, frame_height))
    return plot_image_pil, max_precipitation_value, max_temperature_value
