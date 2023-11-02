# import required python libraries
import os

import logging
# get display from Waveshare library
import epd7in5_V2

# get functions from Pillow
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.DEBUG)

try:
    # initialize display
    epd_disp = epd7in5_V2.EPD()
    epd_disp.init()
    
    # clear display, 0 is black, 255 is white
    epd_disp.Clear()
    
    # reverse width and height as display is sideways
    w = epd_disp.height
    h = epd_disp.width
    print('width', w)
    print('height', h)
    
    #define fonts
    top_font = ImageFont.truetype('Avenir Next.ttc', 18, index=1)
    bottom_font = ImageFont.truetype( 'Avenir Next.ttc', 16, index=5)
    
    # define and draw background
    image = Image.new(mode='1', size=(w, h),color=255)
    draw = ImageDraw.Draw(image)
    
    # position and draw text
    draw.text((15, 0), 'Welcome to the Workshop!', font=top_font, fill=0, align='left')
    draw.text((10, 150), 'https://dronebotworkshop.com', font=bottom_font, fill=0, align='left')
    
    # get robot image 
    dbwsbot = Image.open('H_da_logo_sw.png')
    
    # paste image onto background image
    image.paste(dbwsbot, (80, 35))
    
    # write buffer contents to display
    epd_disp.display(epd_disp.getbuffer(image))
    epd_disp.sleep()
    
except IOError as e:
    print(e)