from PIL import Image, ImageDraw
import logging
import datetime

logging.basicConfig(level=logging.DEBUG)

DEBUG = True
# Define image dimensions
width = 480
height = 800

class WindowManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.img = None
        self.draw = None

    def create_window(self):
        # Create new image object
        self.img = Image.new('RGB', (self.width, self.height), color='white')
        # Draw grid
        self.draw = ImageDraw.Draw(self.img)
        self.draw.line((self.width/2, 0, self.width/2, self.width/2), fill='black', width=2)
        self.draw.line((0, self.width/2, self.width, self.width/2), fill='black', width=2)

    def add_to_window(self, func):
        func(self.img, self.draw)

def add_time(img, draw):
    # Get current time
    now = datetime.datetime.now()
    time_string = now.strftime("%H:%M:%S")
    
    # Write time to top right corner
    draw.text((width - 10, 10), time_string, fill='black')

def main():
    wm = WindowManager(width, height)
    wm.create_window()
    wm.add_to_window(add_time)
    
    # Display image
    if not DEBUG :
        import epd7in5_V2
        epd = epd7in5_V2.EPD()
        epd.init()
        epd.display(epd.getbuffer(wm.img))
        epd.sleep()
    else:
        wm.img.save('output_image.png')
        print('Image saved to output_image.png')

if __name__ == "__main__":
    main()