from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import weather
import get_nextcloud_dat
from config import small_font_name, small_font_size, medium_font_name, medium_font_size, large_font_name, large_font_size, debug
from Dictionaries import months, date_suffix, weekdays
import weather
import date
small_font = ImageFont.truetype(small_font_name, small_font_size)
medium_font = ImageFont.truetype(medium_font_name, medium_font_size)
large_font = ImageFont.truetype(large_font_name, large_font_size)



def create_image():
    # Create a black and white image
    img = Image.new('1', (480, 800), color=1)
    d = ImageDraw.Draw(img)

    # Get current date and time
    #current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Display the date at the top
    #d.text((10, 10), "Date: " + current_date, font=large_font, fill=0)

    # Get plugin data
    weather_img = weather.print_weather()  # Ensure this returns a dictionary or similar structure
    nextcloud_data = get_nextcloud_dat.get_todos()

    # Use the print_date function to create the date section
    date_image = date.print_date()
    
    # Paste the date image onto the main image at the desired location
    img.paste(date_image, (0, 0))  # Adjust the position as necessary

    # Display weather data
    weather_y_start = 100
    # d.text((10, weather_y_start), "Weather Data:", font=medium_font, fill=0)
    # for i, (key, value) in enumerate(weather_data.items()):
    #     d.text((10, weather_y_start + (i+1)*20), f"{key}: {value}", font=medium_font, fill=0)
    img.paste(weather_img, (0, weather_y_start))

    # Loop through each to-do item and display it
    y_position = 260
    for todo in nextcloud_data:
        summary = todo['summary']
        due = datetime.strptime(todo['due'], '%Y-%m-%d %H:%M:%S')
        due_time = due.strftime("%H:%M")
        status = todo['status']

        # Draw the summary text on the image
        d.text((10, y_position), summary, font=large_font, fill=0)
        text_width = d.textlength(summary, font=large_font)

        # Draw the due date on the image
        d.text((text_width+15, y_position+5), due_time, font=medium_font, fill=0)

        # Update the y position for the next to-do item
        y_position += large_font_size + medium_font_size + 4  # Add a small buffer after each to-do item

    # Save or display the image
    img.show()
    # img.save('/path/to/save/image/output_image.bmp')

if __name__ == '__main__':
    create_image()
