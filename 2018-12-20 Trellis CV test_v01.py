# 2018-12-20 Trellis CV test_v01.py
# Based on John Park's classic MIDI example

import board
import busio
import time
from simpleio import map_range
import adafruit_trellism4
import adafruit_adxl34x  # accelerometer

import adafruit_mcp4725  # external DACs

trellis = adafruit_trellism4.TrellisM4Express()
acc_i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA) # for accelerometer
dac_i2c = busio.I2C(board.SCL, board.SDA)  # for DACs

# Initialize accelerometer and DACs
accelerometer = adafruit_adxl34x.ADXL345(acc_i2c)
pitch_dac = adafruit_mcp4725.MCP4725(dac_i2c, address=0x62)
gate_dac = adafruit_mcp4725.MCP4725(dac_i2c, address=0x63)

def wheel(pos):
    dim_factor = 8
    if pos < 0 or pos > 255:
        return 0, 0, 0
    if pos < 85:
        return int(255 - pos * 3)//dim_factor, int(pos * 3)//dim_factor, 0
    if pos < 170:
        pos -= 85
        return 0, int(255 - pos * 3)//dim_factor, int(pos * 3)//dim_factor
    pos -= 170
    return int(pos * 3)//dim_factor, 0, int(255 - (pos * 3)//dim_factor)

for x in range(trellis.pixels.width):
    for y in range(trellis.pixels.height):
        pixel_index = (((y * 8) + x) * 256 // 2)
        trellis.pixels[x, y] = wheel(pixel_index & 255)

current_press = set()

while True:
    pressed = set(trellis.pressed_keys)

    for press in pressed - current_press:
        x, y = press
        print("Pressed:", press)
        noteval = 36 + x + (y * 8)
        print("noteval = ", noteval, int(map_range(noteval, 36, 67, 960, 960+((67-36+1)*(68.25*.75)))))
        pitch_dac.raw_value = int(map_range(noteval, 36, 67, 960, 960+((67-36+1)*(68.25*.75))))
        gate_dac.raw_value = 4095
        time.sleep(0.01)

    for release in current_press - pressed:
        x, y = release
        print("Released:", release)
        noteval = 36 + x + (y * 8)
        gate_dac.raw_value = 0
        time.sleep(0.01)

    current_press = pressed
