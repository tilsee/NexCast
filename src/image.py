from PIL import Image, ImageDraw, ImageFont
import logging
import datetime

logging.basicConfig(level=logging.DEBUG)

DEBUG = False
# Define image dimensions
width = 480
height = 800

class WindowManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.imgs = [None, None, None]
        self.draws = [None, None, None]

    def create_window(self):
        for i in range(3):
            # Create new image object
            self.imgs[i] = Image.new('RGB', (self.width, self.height), color='white')
            # Draw grid
            self.draws[i] = ImageDraw.Draw(self.imgs[i])
            self.draws[i].line((self.width/2, 0, self.width/2, self.width/2), fill='black', width=2)
            self.draws[i].line((0, self.width/2, self.width, self.width/2), fill='black', width=2)

    def add_to_window(self, input_img, window_number):
        # Scale image to fit window
        input_img.thumbnail((self.width, self.height))
        # Add image to window
        self.imgs[window_number].paste(input_img, (0, 0))

def add_time():
    # Get current time
    now = datetime.datetime.now()
    time_string = now.strftime("%H:%M:%S")
    
    # Create new image object
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Write time to top right corner
    draw.text((0, 10), time_string, fill='black')
    
    return img

def main():
    wm = WindowManager(width, height)
    wm.create_window()
    wm.add_to_window(add_time(), 0)
    
    # Display image
    if not DEBUG :
        import epd7in5_V2
        epd = epd7in5_V2.EPD()
        epd.init()
        for img in wm.imgs:
            epd.display(epd.getbuffer(img))
        epd.sleep()
    else:
        for i, img in enumerate(wm.imgs):
            img.save(f'output_image_{i}.png')
        print('Images saved to output_image_0.png, output_image_1.png, output_image_2.png')

if __name__ == "__main__":
    main()