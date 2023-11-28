from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import weather
import get_nextcloud_dat
from config import small_font_name, small_font_size, medium_font_name, medium_font_size, large_font_name, large_font_size, debug, ical_urls
import weather
import date
import sys
import os
from dateutil import tz

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Add the script directory to the Python path
sys.path.append(script_directory)

small_font = ImageFont.truetype(small_font_name, small_font_size)
medium_font = ImageFont.truetype(medium_font_name, medium_font_size)
large_font = ImageFont.truetype(large_font_name, large_font_size)



def create_base_image():
    img = Image.new('1', (480, 800), color=1)
    d = ImageDraw.Draw(img)
    return img, d

def paste_date_section(img, now):
    date_image = date.print_date(now = now)
    img.paste(date_image, (0, 0))  # Adjust the position as necessary
    return img

def paste_weather_data(img, weather_data):
    weather_img, max_precip, max_temp = weather.plot_weather(weather_data)
    weather_y_start = 100
    img.paste(weather_img, (0, weather_y_start))
    return img

def str_len_5_conv(string):
    if len(string) >= 5:
        return string[:5]
    else:
        str_len_diff = 5-len(string)
        string = string + ' '*str_len_diff*7
        return string

def draw_todo_items(d, img, nextcloud_data, weather_data):
    y_position = 260
    i = 1
    for todo in nextcloud_data:
        summary = todo['summary'][:10]
        calendar_name = str_len_5_conv(todo['calendar'])
        try:
            tstart = todo['due']
            tend = todo['end_date']
            due = datetime.strptime(tstart, '%Y-%m-%d %H:%M:%S')
            due_time = due.strftime("%H:%M")
        except:  due = due_time = ''

        icon = weather.get_icon(tstart, tend, weather_data)
        d.text((0, y_position), str(i)+'.', font=large_font, fill=0)
        d.text((30, y_position), calendar_name, font=large_font, fill=0)
        d.text((115, y_position), ': '+summary, font=large_font, fill=0)
        i += 1
        x_time = 400
        d.text((x_time, y_position+5), due_time, font=medium_font, fill=0)
        if icon is not None:
            icon = icon.convert("1") 
            img.paste(icon, (x_time-20, y_position+5))
        y_hline = y_position
        d.line((0, y_hline, 480, y_hline), fill=0)
        y_position += large_font_size + 8  # Add a small buffer after each to-do item
    return d

def add_current_time(d, now):
    current_time = now.strftime("%H:%M")
    time_width= d.textlength(current_time, font=large_font)
    x_position = 480 - time_width
    d.text((x_position, 0), current_time, font=large_font, fill=0)
    return d

def create_image(rotate=False):
    local_tz = tz.tzlocal()
    # get data:
    now = datetime.now(tz=local_tz)
    calendars = get_nextcloud_dat.fetch_all_events(now = now, ical_urls=ical_urls)
    weather_data = weather.get_weather(now)

    # create image:
    img, d = create_base_image()
    img = paste_date_section(img, now)
    img = paste_weather_data(img, weather_data)
    d = add_current_time(d, now)
    d = draw_todo_items(d, img, calendars, weather_data)
    if rotate:
            img = img.rotate(180)
    return img

if __name__ == '__main__':
    img = create_image()
    img.show()