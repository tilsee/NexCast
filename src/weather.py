import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from io import BytesIO
from PIL import Image
from datetime import datetime, timedelta
import requests
from config import open_meteo_url
import sys
import os

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Add the script directory to the Python path
sys.path.append(script_directory)


def get_weather():
    url = open_meteo_url
    response = requests.get(url)
    data = response.json()['minutely_15']
    output_data = {}
    now = datetime.now()
    for i in range(len(data['temperature_2m'])):
        time = datetime.fromisoformat(data['time'][i])
        if time > now and time < now + timedelta(hours=24):
            output_data[time] = { 'temperature': data['temperature_2m'][i], 'percipitation': data['precipitation'][i] }
    return output_data

def customize_plot(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', which='both', left=False, labelleft=False, right=False, labelright=False)
    ax.xaxis.set_major_formatter(DateFormatter('%H'))

def annotate_max_values(ax, data, color, max_value, xytext_offset):
    max_date = None
    for date, value in data.items():
        if value == max_value:
            max_date = date
            break
    if max_date is not None and max_value is not None:
        ax.annotate(f'{str(round(max_value,2))}', xy=(max_date, max_value), xytext=xytext_offset, 
                    textcoords='offset points', ha='center', color=color)
        
def get_icon(data):
    pass

def plot_weather():
    frame_width, frame_height = (480, 150)
    next_24h_data = get_weather()
    dates = list(next_24h_data.keys())
    percipitation = [next_24h_data[date]['percipitation'] for date in dates]
    temperature = [next_24h_data[date]['temperature'] for date in dates]

    if not next_24h_data:
        return "No data available for the next 24 hours.", None, None

    fig, ax1 = plt.subplots(figsize=(frame_width/124, frame_height/124), dpi=124)
    customize_plot(ax1)

    ax1.bar(dates, percipitation, color='black', width=0.03)
    ax1.set_ylim(bottom=0)
    ax2 = ax1.twinx()
    ax2.plot(dates, temperature, color='grey')
    ax2.set_ylim(bottom=0)
    customize_plot(ax2)

    max_precipitation_value = max(percipitation)
    max_temperature_value = max(temperature)

    annotate_max_values(ax1, dict(zip(dates,percipitation)), 'black', max_precipitation_value, (-10, 10))
    annotate_max_values(ax2, dict(zip(dates,temperature)), 'grey', max_temperature_value, (10, 10))

    plt.tight_layout()
    plt.subplots_adjust(left=0.1, bottom=0.136, right=0.926, top=0.99)

    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    plot_image_pil = Image.open(buf).resize((frame_width, frame_height))
    return plot_image_pil, max_precipitation_value, max_temperature_value
