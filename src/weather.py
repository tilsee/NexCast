import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import datetime
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

def print_weather():
    frame_width, frame_height = (480, 150)
    hourly_dataframe = get_weather()  # Ensure this function returns the weather data as a DataFrame.
    
    # Convert 'date' column to datetime and filter for the next 24 hours.
    hourly_dataframe['date'] = pd.to_datetime(hourly_dataframe['date'])
    current_time = pd.Timestamp.now().floor('H')
    mask = (hourly_dataframe['date'] >= current_time) & (hourly_dataframe['date'] < current_time + pd.Timedelta(hours=24))
    next_24h_data = hourly_dataframe.loc[mask]

    if next_24h_data.empty:
        raise ValueError("No data available for the next 24 hours.")

    # Plot the data
    fig, ax1 = plt.subplots(figsize=(frame_width/124, frame_height/124), dpi=124)

    # Plot precipitation
    ax1.bar(next_24h_data['date'], next_24h_data['precipitation'], color='black', label='Precipitation', width=0.03)
    ax1.set_ylim(bottom=0)

    # Create a twin axis for temperature
    ax2 = ax1.twinx()

    # Plot temperature on the twin axis
    ax2.plot(next_24h_data['date'], next_24h_data['temperature_2m'], color='grey', label='Temperature')
    ax2.set_ylim(bottom=0)

    # Formatting x-axis
    hoursFmt = DateFormatter('%H')
    ax1.xaxis.set_major_formatter(hoursFmt)

    # Hide all spines
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)

    # Hide y-ticks and labels
    ax1.tick_params(axis='y', which='both', left=False, labelleft=False)
    ax2.tick_params(axis='y', which='both', right=False, labelright=False)

    # Hide the labels and legend
    ax1.set_ylabel('')
    ax2.set_ylabel('')
    ax1.legend().set_visible(False)
    ax2.legend().set_visible(False)

    # Find the maximum values for precipitation and temperature
    max_precipitation_value = round(next_24h_data['precipitation'].max(),2)
    max_temperature_value = round(next_24h_data['temperature_2m'].max(),2)
    print 
    # Check if the maximum values are not NaN and the DataFrame is not empty
    if pd.notna(max_precipitation_value) and pd.notna(max_temperature_value):
        # Find the index for the maximum values
        max_precipitation_idx = next_24h_data['precipitation'].idxmax()
        max_temperature_idx = next_24h_data['temperature_2m'].idxmax()

        #Annotate the maximum values on the plot
        ax1.annotate(f'{str(max_precipitation_value)}', 
                     xy=(next_24h_data.loc[max_precipitation_idx, 'date'], max_precipitation_value), 
                     xytext=(0, 10), textcoords='offset points', ha='center', va='bottom', color='black')
        ax2.annotate(f'{str(max_temperature_value)}', 
                     xy=(next_24h_data.loc[max_temperature_idx, 'date'], max_temperature_value), 
                     xytext=(0, 10), textcoords='offset points', ha='center', va='bottom', color='grey')
    else:
        # Handle the case where the maximum values are NaN or the DataFrame is empty
        print("No valid maximum value to annotate.")

    # Display the plot with minimal padding
    plt.tight_layout()
    plt.subplots_adjust(left=0.1, bottom=0.136, right=0.926, top=0.99)

    # Save plot to a BytesIO buffer
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    plot_image_pil = Image.open(buf)

    # Ensure the image is resized to the specified dimensions if necessary
    plot_image_pil = plot_image_pil.resize((frame_width, frame_height))
    # Return the PIL Image object
    return plot_image_pil

