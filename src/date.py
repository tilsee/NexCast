from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from Dictionaries import months, date_suffix, weekdays
from config import small_font_name, small_font_size, medium_font_name, medium_font_size, large_font_name, large_font_size, debug

def get_date():
    now = datetime.now()
    day_suffix = date_suffix.get(str(now.day), 'th')
    return {
        'weekday': weekdays[str(now.isoweekday())],
        'day': str(now.day),
        'month': months[str(now.month)],
        'year': str(now.year),
        'day_suffix': day_suffix
    }
    
def print_date(width=240, height=240, angle=0, large_font_size=20, medium_font_size=15):
    # Create the date image and draw object
    h_black_image = Image.new('1', (width, height), 255)
    draw_date = ImageDraw.Draw(h_black_image)
    date = get_date()

    # Use your font configurations
    large_font = ImageFont.truetype(large_font_name, large_font_size)
    medium_font = ImageFont.truetype(medium_font_name, medium_font_size)
    h_black_image = Image.new('1', (width, height), 255)
    draw_date = ImageDraw.Draw(h_black_image)
    date = get_date()

    # Calculate the dimensions of the first text
    text_width1 = draw_date.textlength(date['weekday'], font=large_font)
    text_height1 = large_font_size

    # Calculate the dimensions of the second text
    text_width2 = draw_date.textlength(date['month'] + ' ' + date['day'] + date_suffix[date['day']] + ' ' + date['year'], font=medium_font)
    text_height2 = medium_font_size

    # Calculate the center of the image
    center_x = width // 2
    center_y = height // 2

    # Calculate the new coordinates to center the texts
    x1_centered = center_x - text_width1 / 2
    y1_centered = center_y - text_height1 / 2

    x2_centered = center_x - text_width2 / 2
    y2_centered = center_y - text_height2 / 2

    # Create a new image to group the texts
    grouped_image = Image.new('1', (width, height), 255)
    draw_group = ImageDraw.Draw(grouped_image)

    # Draw the first text on the grouped image
    draw_group.text((x1_centered-54, y1_centered-104),
                    date['weekday'],
                    font=large_font,
                    fill=0)

    # Draw the second text on the grouped image
    draw_group.text((x2_centered-13, y2_centered-83),
                    date['month'] + ' ' + date['day'] + date_suffix[date['day']] + ' ' + date['year'],
                    font=medium_font,
                    fill=0)

    # Rotate the grouped image
    rotated_grouped_image = grouped_image.rotate(angle, expand=True)

    # Paste the rotated grouped image onto the original image
    h_black_image.paste(rotated_grouped_image, (0, 0))

    return h_black_image    
