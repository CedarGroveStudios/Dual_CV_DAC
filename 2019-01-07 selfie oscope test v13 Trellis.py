# 2019-01-07 selfie oscope test v13 Trellis.py
# oscilloscope x-y graphics test
#
# 2019 Cedar Grove Studios
# from Cedar Grove's CircuitPython StringCar Racer project
# adapted for John Park's workshop 3/29/2018 pan/tilt project
# modified for dual DAC output to drive oscilloscope

# ### Setup ###
import board

import time
import neopixel as neo
from analogio import AnalogIn, AnalogOut

import busio
import adafruit_mcp4725

ext_i2c = busio.I2C(board.SCL, board.SDA)  # for DACs
x_out = adafruit_mcp4725.MCP4725(ext_i2c, address=0x62)
y_out = adafruit_mcp4725.MCP4725(ext_i2c, address=0x63)

# set up x-y scope output pins
# x_out = AnalogOut(board.A0)
# y_out = AnalogOut(board.A1)

# dim the on-board neopixel and show yellow start-up indicator
pixel = neo.NeoPixel(board.NEOPIXEL,1, brightness=0.01, auto_write=False)
pixel[0] = (128, 128, 0)
pixel.write()

trellis_outline = [  # raw, absolute 12-bit data points
    (0, 0),
    (0, 41520),
    (21760, 41520),
    (21760, 36000),
    (43520, 36000),
    (43520, 41520),
    (65280, 41520),
    (65280, 0)
    ]

button_outline = [  # raw, relative 12-bit data points
    (0, 0),
    (0, 6000),
    (6000, 6000),
    (6000, 0)
    ]

print("2019-01-07 selfie oscope test v13 Trellis.py")

button = 1
d = 0

while True:
    for i in range(0, 8):
        x, y = trellis_outline[i]
        x_out.value = x
        y_out.value = y
        time.sleep(d)
    for j in range(0, 8):
        x_offset = 1920 + (7920 * j)
        for k in range(0, 4):
            y_offset = 1920 + (7920 * k)
            for m in range(0, 4):
                x, y = button_outline[m]
                x_out.value = (x + x_offset)
                y_out.value = (y + y_offset)
                time.sleep(d)
            if button == j + (k * 8):
                x,y = button_outline[1]
                x_out.value = ((x//2) + x_offset)
                y_out.value = ((y//2) + y_offset)
                time.sleep(d)
                x,y = button_outline[2]
                x_out.value = ((x//2) + x_offset)
                y_out.value = ((y//2) + y_offset)
                time.sleep(d)
                x,y = button_outline[0]
                x_out.value = ((x//2) + x_offset)
                y_out.value = ((y//2) + y_offset)
                time.sleep(d)
