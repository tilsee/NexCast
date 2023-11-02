from PIL import Image, ImageDraw
DEBUG = True
# Define image dimensions
width = 480
height = 800

# Create new image object
img = Image.new('RGB', (width, height), color='white')

# Draw grid
draw = ImageDraw.Draw(img)
# Draw horizontal line
draw.line((width/2, 0, width/2, width/2), fill='black', width=2)
# Draw vertical line
draw.line((0, width/2, width, width/2), fill='black', width=2)

# save image

if not DEBUG :
    # Display image
    import epd7in5_V2
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.display(epd.getbuffer(img))
    epd.sleep()
else:
    img.save('output_image.png')
    print('Image saved to output_image.png')