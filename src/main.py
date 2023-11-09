import frame_gen
from lib import epd7in5_V2
epd = epd7in5_V2.EPD()
epd.init()

def main():
    img = frame_gen.create_image()
    epd.display(epd.getbuffer(img))
    epd.sleep()

if __name__ == '__main__':
    main()