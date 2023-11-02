from PIL import ImageDraw, Image, ImageOps, ImageEnhance, ImageFont

from config import small_font_name, small_font_size, medium_font_name, medium_font_size, large_font_name, large_font_size
import epd7in5_V2

epd = epd7in5_V2.EPD()
# epd.init()

hight = epd7in5_V2.EPD_HEIGHT
width = epd7in5_V2.EPD_WIDTH

h_black_image = Image.new('1', (hight, width), 255)
draw_black = ImageDraw.Draw(h_black_image)

#small_font = ImageFont.truetype(small_font_name, small_font_size)
#medium_font = ImageFont.truetype(medium_font_name, medium_font_size)
#large_font = ImageFont.truetype(large_font_name, large_font_size)

print(hight, width)