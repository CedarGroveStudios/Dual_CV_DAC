# 2019-01-06 circle oscope test v13 Trellis.py
# oscilloscope x-y graphics test
#
# 2019 Cedar Grove Studios

# ### Setup ###
import board
from math import sin, cos, pi
import busio
import adafruit_mcp4725

import time
import neopixel as neo
from analogio import AnalogIn, AnalogOut

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

print("2019-01-06 circle oscope test v13 Trellis.py")

res = 128

while True:
    for i in range(0, int(2 * pi * res)):
        x_out.value = int(cos(i/res) * 65535//2) + 65536//2
        y_out.value = int(sin(i/res) * 65535//2) + 65536//2


    