import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from io import BytesIO
from PIL import Image
from datetime import datetime, timedelta, timezone
import requests
from config import open_meteo_url
import sys
import os
from PIL import Image
import matplotlib
import matplotlib.dates as mdates
from dateutil import tz

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Add the script directory to the Python path
sys.path.append(script_directory)


def get_weather(now = None):
    if now is None:
        now = datetime.now(timezone.utc)
    url = open_meteo_url
    response = requests.get(url)
    data = response.json()['minutely_15']
    output_data = {}
    for i in range(len(data['temperature_2m'])):
        time = datetime.fromisoformat(data['time'][i]).replace(tzinfo=tz.tzlocal())
        if now <= time < now + timedelta(hours=24):
            output_data[time] = {'temperature': data['temperature_2m'][i], 'percipitation': data['precipitation'][i]}
    return output_data

def customize_plot(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', which='both', left=False, labelleft=False, right=False, labelright=False)
    ax.xaxis.set_major_formatter(DateFormatter('%H'))

def annotate_max_values(ax, data, color, max_value, x_pos, xytext_offset, unit=''):
    max_date_float = matplotlib.dates.date2num(x_pos)  # Convert max_date to float
    if max_date_float < ax.get_xlim()[1] - ax.get_xlim()[0]:
        xytext_offset = (xytext_offset[0] * -1, xytext_offset[1])
    ax.annotate(f'{str(round(max_value,2))+ unit}', xy=(x_pos, max_value), xytext=xytext_offset, 
                textcoords='offset points', ha='center', color=color)
        
def will_it_rain(weather_data, start_time, end_time):
    rain_status = 0
    if type(start_time) == str:
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").replace(tzinfo=tz.tzlocal())
    if type(end_time) == str:
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S").replace(tzinfo=tz.tzlocal())
    
    for date_key in weather_data:
        if start_time <= date_key <= end_time:
            if weather_data[date_key]['percipitation'] > 0:
                rain_status = 1
                break
    return rain_status

def get_icon(startTime, endTime, weather_data):
    res = will_it_rain(weather_data, startTime, endTime)

    # Load the image
    image = Image.open("lib/umbrella.png").convert('RGBA')

    # Separate the alpha channel from the RGB channels
    rgb_image = image.convert('RGB')

    # Convert the RGB image to black and white
    bw_image = rgb_image.convert('L').point(lambda x: 0 if x<128 else 255, '1')

    resized_image = bw_image.resize((20, 20))
    if res == 1 : 
        return resized_image
    else: return None

def plot_weather(next_24h_data=None):
    frame_width, frame_height = (480, 150)
    dates = list(next_24h_data.keys())
    percipitation = [next_24h_data[date]['percipitation'] for date in dates]
    temperature = [next_24h_data[date]['temperature'] for date in dates]

    if not next_24h_data:
        return "No data available for the next 24 hours.", None, None

    fig, ax1 = plt.subplots(figsize=(frame_width/124, frame_height/124), dpi=124)
    customize_plot(ax1)

    ax1.bar(dates, percipitation, color='black', width=0.03)
    ax1.set_ylim(bottom=0)
    ax1.set_xlim([min(dates), max(dates)])  # Set x-axis limits

    ax2 = ax1.twinx()
    ax2.plot(dates, temperature, color='grey')
    ax2.set_xlim([min(dates), max(dates)])  # Set x-axis limits
    ax2.axhline(0, color='blue', linewidth=0.5)  # Add horizontal line at zero degrees
    customize_plot(ax2)

    max_precipitation_value = max(percipitation)
    max_temperature_value = max(temperature)

    annotate_max_values(ax1, dict(zip(dates,percipitation)), 'black', max_precipitation_value, max(dates),(-25  , 10), 'mm')
    annotate_max_values(ax2, dict(zip(dates,temperature)), 'gray', max_temperature_value, min(dates),(20, 10),'°C')

    plt.tight_layout()
    plt.subplots_adjust(left=0.1, bottom=0.136, right=0.926, top=0.99)

    # Format x-axis ticks as hours
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H'))

    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    plot_image_pil = Image.open(buf).resize((frame_width, frame_height))
    return plot_image_pil, max_precipitation_value, max_temperature_value