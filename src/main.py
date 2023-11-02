#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import logging
import epd7in5_V2
from PIL import Image

logging.basicConfig(level=logging.DEBUG)

def init_epd():
    logging.info("epd7in5_V2 Demo")
    epd = epd7in5_V2.EPD()
    return epd

def clear_epd(epd):
    epd.Clear()

def load_image(image_path, epd):
    image = Image.open(image_path)
    image.thumbnail((epd.width, epd.height))
    return image

def display_image(epd, image):
    epd.display(epd.getbuffer(image))

def main():
    epd = init_epd()
    try:
        logging.info("Clear...")
        epd.init()
        clear_epd(epd)
        image = load_image('H_da_logo_sw.png', epd)
        display_image(epd, image)
    except KeyboardInterrupt:
        pass
    finally:
        logging.info("Goto Sleep...")
        epd.sleep()

if __name__ == "__main__":
    main()