import frame_gen
from lib import epd7in5_V2
epd = epd7in5_V2.EPD()

def main():
    try :
        img = frame_gen.create_image()
        epd.init()
        epd.display(epd.getbuffer(img))
    except:
        epd.init()
        epd.Clear()
    finally:
        epd.sleep()

if __name__ == '__main__':
    main()