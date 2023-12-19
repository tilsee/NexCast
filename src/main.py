import argparse
import frame_gen
from lib import epd7in5_V2

epd = epd7in5_V2.EPD()

def main(clear_display):
    if clear_display:
        epd.init()
        epd.Clear()
        epd.sleep()
    else:
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--clear', action='store_true', help='Clear the display')
    args = parser.parse_args()
    main(args.clear)