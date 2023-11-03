from PIL import Image, ImageDraw, ImageFont
import datetime
from config import small_font_name, small_font_size, medium_font_name, medium_font_size, large_font_name, large_font_size
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
        # Draw horizontal grid lines
        line_y = 240
        while line_y < 800:
            self.draw_black.line([(0, line_y), (480, line_y)], fill=0)
            line_y += 80

        # Draw the line splitting the top section into two squares
        self.draw_black.line([(0, 240), (480, 240)], fill=0)

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
        import epd7in5_V2
        epd = epd7in5_V2. EPD()
        epd.init ()
        epd.display(epd.getbuffer(self.h_black_image))
        epd.sleep()

    def save_frame(self, filename):
       self.h_black_image.save(filename)
       print("Frame saved to", filename)

from PIL import Image, ImageDraw, ImageFont
import datetime

def print_date():
    h_black_image = Image.new('1', (240, 240), 255)
    draw_date = ImageDraw.Draw(h_black_image)
    date = get_date()
    w = draw_date.textlength(date['weekday'], font=large_font)
    draw_date.text((2, 2),
				  date['weekday'],
				  font=large_font,
				  fill=0)
    draw_date.text((w + 7, 5),
					months[date['month']] + ' ' + date['day'] + date_suffix[date['day']] + ' ' + date['year'],
					font=medium_font,
					fill=0)
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

    image2 = Image.open("dbws-robot.bmp")
    image3 = Image.open("dbws-robot.bmp")

    # Allocate images to specific windows
    frame.allocate_window(image2, window_number=2)
    frame.allocate_window(image3, window_number=3)

    if False:
        frame.refresh_display()

    # Save the frame
    frame.save_frame("output_frame.png")
