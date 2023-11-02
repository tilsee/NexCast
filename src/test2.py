import os
import logging
import epd7in5_V2
from PIL import Image, ImageDraw, ImageFont, ImageOps

logging.basicConfig(level=logging.DEBUG)
w = None
h = None
def init_epd():
    epd_disp = epd7in5_V2.EPD()
    epd_disp.init()
    return epd_disp

def clear_epd(epd_disp):
    epd_disp.Clear()

def create_image(epd_disp):
    global w, h
    w = epd_disp.height
    h = epd_disp.width
    img = ImageOps.invert(img)  # invert colors
    return Image.new(mode='1', size=(w, h), color=255)

def draw_text(image, text, position, font_path, font_size, font_index):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size, index=font_index)
    draw.text(position, text, font=font, fill=0, align='left')

def add_image(image, image_path, position):
    img = Image.open(image_path)
    img.thumbnail((w,h))
    img = img.convert('1')
    image.paste(img, position)

def display_image(epd_disp, image):
    epd_disp.display(epd_disp.getbuffer(image))
    epd_disp.sleep()

def main():
    try:
        epd_disp = init_epd()
        clear_epd(epd_disp)
        image = create_image(epd_disp)
        draw_text(image, 'Welcome to the Workshop!', (15, 0), 'Avenir Next.ttc', 18, 1)
        draw_text(image, 'https://dronebotworkshop.com', (10, 150), 'Avenir Next.ttc', 16, 5)
        add_image(image, 'H_da_logo_sw.png', (80, 35))
        display_image(epd_disp, image)
    except IOError as e:
        print(e)

if __name__ == "__main__":
    main()