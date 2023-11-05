from PIL import Image, ImageDraw, ImageFont
import datetime
from config import small_font_name, small_font_size, medium_font_name, medium_font_size, large_font_name, large_font_size, debug
from Dictionaries import months, date_suffix, weekdays

small_font = ImageFont.truetype(small_font_name, small_font_size)
medium_font = ImageFont.truetype(medium_font_name, medium_font_size)
large_font = ImageFont.truetype(large_font_name, large_font_size)


class FrameWithGrid:
    def __init__(self):
        self.h_black_image = Image.new('1', (480, 800), 255)
        self.draw_black = ImageDraw.Draw(self.h_black_image)
        self.draw_grid_lines()

    def draw_grid_lines(self):
        # Draw horizontal grid line
        self.draw_black.line([(240, 0), (240, 240)], fill=0)
        # Draw the line splitting the top section into two squares
        self.draw_black.line([(0, 240), (480, 240)], fill=0)
        pass

    def allocate_window(self, img, window_number=None):
        if window_number is None:
            window_number = 1

        if window_number == 1:
            img = img.resize((240, 240))
            self.h_black_image.paste(img, (0, 0))
        elif window_number == 2:
            img = img.resize((240, 240))
            self.h_black_image.paste(img, (240, 0))
        elif window_number == 3:
            img = img.resize((480, 560))
            self.h_black_image.paste(img, (0, 240))
        else:
            raise ValueError("Invalid window number. Choose from 1, 2, or 3.")
    
    def refresh_display(self):
        from lib import epd7in5_V2
        epd = epd7in5_V2. EPD()
        epd.init ()
        epd.display(epd.getbuffer(self.h_black_image))
        epd.sleep()

    def save_frame(self, filename):
       self.h_black_image.save(filename)
       print("Frame saved to", filename)

def print_date(width=240, height=240, angle=12):
    h_black_image = Image.new('1', (width, height), 255)
    draw_date = ImageDraw.Draw(h_black_image)
    date = get_date()

    # Calculate the dimensions of the first text
    text_width1 = draw_date.textlength(date['weekday'], font=large_font)
    text_height1 = large_font_size

    # Calculate the dimensions of the second text
    text_width2 = draw_date.textlength(months[date['month']] + ' ' + date['day'] + date_suffix[date['day']] + ' ' + date['year'], font=medium_font)
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
                    months[date['month']] + ' ' + date['day'] + date_suffix[date['day']] + ' ' + date['year'],
                    font=medium_font,
                    fill=0)

    # Rotate the grouped image
    rotated_grouped_image = grouped_image.rotate(angle, expand=True)

    # Paste the rotated grouped image onto the original image
    h_black_image.paste(rotated_grouped_image, (0, 0))

    return h_black_image    

def get_date():
	now = datetime.datetime.now()
	return {
		'weekday': weekdays[str(now.isoweekday())],
		'day': str(now.day),
		'month': str(now.month),
		'year': str(now.year)
	}

# Example usage:
if __name__ == "__main__":
    frame = FrameWithGrid()

    # Create an image with the current time
    time_image = print_date()

    # Allocate the time image to window 1
    frame.allocate_window(time_image, window_number=1)
    frame.allocate_window(time_image, window_number=3)
    frame.allocate_window(time_image, window_number=2)
    frame.draw_grid_lines()

    image2 = Image.open("assets/dbws-robot.bmp")
    image3 = Image.open("assets/dbws-robot.bmp")

    # Allocate images to specific windows
    #frame.allocate_window(image2, window_number=2)
    #frame.allocate_window(image3, window_number=3)

    if False:
        frame.refresh_display()

    # Save the frame
    frame.save_frame("output_frame.png")
