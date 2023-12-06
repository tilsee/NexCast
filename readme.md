# About the Project
This project has the goal to create a smart e-paper display to display a To-Do List and some other rudimentary information like weather data
# Used Hardware
In the first poc a raspberry pi 2b is used as well as a 7.5inch ePaper screen from [waveshare](https://www.waveshare.com/product/7.5inch-e-paper-hat.htm
)

This project was partly inspired by [zoharsf](https://github.com/zoharsf/Raspberry-Pi-E-Ink-Dashboard)

# Getting started

## requirements

Several packages are required to run this project. The following packages are required:
sudo apt-get install libxslt1-dev
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo apt-get install python-matplotlib
sudo pip3 install RPi.GPIO
sudo pip3 install spidev


## Installation

To get started, you'll need to install several packages. The  [documentation](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_Manual#Demo_code) from Waveshare covers most of the necessary steps: 
It is also strongly recommended to run the demo code to check if everything works before runing this project.

However, if you're using a virtual environment, it's recommended to install several packages from pip instead of the package manager apt. Additionally, you'll need to install the apt-get package **libopenjp2-7**.

## Running the code

To run the code in this repository, you'll need to copy the files **epdconfig.pyc**, 
**epdconfig.py** **epd7in5_V2.py** and **epd7in5_V2.pyc** from the [Waveshare e-Paper](https://github.com/waveshareteam/e-Paper/tree/master) repository into the root directory of this repository. The path to the files is **RaspberryPi_JetsonNano/python/lib/waveshare_epd/**.

## Automating using cronjob

using `crontab -e` add the following line to the end of the file:
```
*/15 * * * * cd /home/imenoxs/NexCast/src && /usr/bin/python /home/imenoxs/NexCast/src/main.py >> /home/imenoxs/NexCast/src/cron.log 2>&1
```

refreshes all 15 min and logs output to cron.log file inside repo