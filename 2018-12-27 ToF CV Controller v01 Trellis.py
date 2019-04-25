# 2018-12-27 ToF CV Controller v01 Trellis.py
# simple demo of the VL53L0X distance sensor
# with the 4-digit alphanumeric LED Feather Wing
#

import time
import random as rnd
import digitalio
from analogio import AnalogIn, AnalogOut
import board
import busio

import adafruit_trellism4
import adafruit_adxl34x  # accelerometer

import adafruit_mcp4725  # external DACs
import adafruit_vl53l0x
from adafruit_ht16k33 import segments

import microcontroller  # for checking CPU temperature
import gc  # for checking memory capacity
from simpleio import map_range

trellis = adafruit_trellism4.TrellisM4Express()
# Initialize external and internal I2C bus, sensor, and display
acc_i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA) # for accelerometer
ext_i2c = busio.I2C(board.SCL, board.SDA)  # for DACs

# Initialize accelerometer and DACs
accelerometer = adafruit_adxl34x.ADXL345(acc_i2c)
pitch_dac = adafruit_mcp4725.MCP4725(ext_i2c, address=0x62)
gate_dac = adafruit_mcp4725.MCP4725(ext_i2c, address=0x63)
vl53 = adafruit_vl53l0x.VL53L0X(ext_i2c)
display = segments.Seg14x4(ext_i2c)

gate_dac.value = 0
pitch_dac.value = 0

#vl53.measurement_timing_budget = 33000  # default: compromise
#vl53.measurement_timing_budget = 20000  # fast and inaccurate
#vl53.measurement_timing_budget = 200000  # slow and accurate

# ### Setup ###

# ### Dictionaries and Lists ###

# ### Helpers ###
def plot(plot_val):
    if plot_val < 0: plot_val = 0
    if plot_val >31: plot_val = 31
    x = plot_val % 8
    y = int(plot_val/8) % 4
    return x, y

# ### Main ###
print("2018-12-27 ToF CV Controller v01 Trellis.py")
print("GC.mem_free:  %0.3f" % float(gc.mem_free()/1000), "KB")
print("CPU.freqency:   %0.1f" % float(microcontroller.cpu.frequency/1000000), "MHz")
print("CPU.temperature: %0.1f" % microcontroller.cpu.temperature, "C")

display.fill(0)
display.print('CG-1')
display.show()
time.sleep(1)
display.print('   -')
display.show()

for x in range(trellis.pixels.width):
    for y in range(trellis.pixels.height):
        trellis.pixels[x, y] = 0x000008  # light blue background

for i in range(0, 32):
    trellis.pixels[plot(i)] = 0x000008
    time.sleep(0.05)

depth = 800  # active sensitivity distance in mm
old_range = 0

while True:
    range = vl53.range
    if range <= depth:
        x,y = plot(int(map_range(range, 100, depth, 0, 32)))
        display.print(range)
        display.show()
        trellis.pixels[x, y] = 0x323200
        pitch_dac.value = int((65535/2)+(65520/2 * range / depth))
        old_range = range
        gate_dac.value = 65520
        time.sleep(.04)  # gate duration
        gate_dac.value = 0
        trellis.pixels[x, y] = 0x080000
    else:
        if range < 2000:
            display.print(range)
            display.show()
        time.sleep(0.1)  # time before erasing neos
        gate_dac.value = 0
        for i in range(0, 32):
            trellis.pixels[plot(i)] = 0x000008
        display.fill(0)
        display[3] = '-'
        display.show()
    time.sleep(0)
