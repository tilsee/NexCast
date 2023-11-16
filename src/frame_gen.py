from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import weather
import get_nextcloud_dat
from config import small_font_name, small_font_size, medium_font_name, medium_font_size, large_font_name, large_font_size, debug
import weather
import date
small_font = ImageFont.truetype(small_font_name, small_font_size)
medium_font = ImageFont.truetype(medium_font_name, medium_font_size)
large_font = ImageFont.truetype(large_font_name, large_font_size)



def create_base_image():
    img = Image.new('1', (480, 800), color=1)
    d = ImageDraw.Draw(img)
    return img, d

def paste_date_section(img):
    date_image = date.print_date()
    img.paste(date_image, (0, 0))  # Adjust the position as necessary
    return img

def paste_weather_data(img):
    weather_img, max_precip, max_temp = weather.plot_weather()
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

def draw_todo_items(d, nextcloud_data):
    y_position = 260
    i = 1
    for todo in nextcloud_data:
        summary = todo['summary'][:20]
        calendar_name = str_len_5_conv(todo['calendar'])
        try:
            due = datetime.strptime(todo['due'], '%Y-%m-%d %H:%M:%S')
            due_time = due.strftime("%H:%M")
        except:  due = due_time = ''
        d.text((0, y_position), str(i)+'.', font=large_font, fill=0)
        d.text((25, y_position), calendar_name, font=large_font, fill=0)
        d.text((115, y_position), ': '+summary, font=large_font, fill=0)
        #todo_txt = f'{i}. {calendar_name}: {summary}'
        i += 1
        #d.text((10, y_position), todo_txt, font=large_font, fill=0)
        #text_width = d.textlength(todo_txt, font=large_font)
        x_time = 400
        d.text((x_time, y_position+5), due_time, font=medium_font, fill=0)
        y_hline = y_position
        d.line((0, y_hline, 480, y_hline), fill=0)
        y_position += large_font_size + 8  # Add a small buffer after each to-do item
    return d

def create_image():
    img, d = create_base_image()
    img = paste_date_section(img)
    img = paste_weather_data(img)
    d = draw_todo_items(d, get_nextcloud_dat.fetch_calendar_entries())
    return img

if __name__ == '__main__':
    img = create_image()
    img.show()