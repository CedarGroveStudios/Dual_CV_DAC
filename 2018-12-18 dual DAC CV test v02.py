# 2018-12-18 dual DAC CV test v02.py
# 
# 2018-12-18 test of Stemma dual DAC  -- Cedar Grove Studios
#

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

# There are a three ways to set the DAC output, you can use any of these:
# dac2.value = 65535
# dac2.raw_value = 4095
# dac2.normalized_value = 1.0

step_delay = 0.0

print("2018-12-18 dual DAC CV test v02.py")

while True:
    x, y, z = accelerometer.acceleration
    # print((x,y,z))
    
    new_y = int(map_range(x, -10, 10, 0, 65520))
    new_x = int(map_range(y, 10, -10, 0, 65520))
    new_z = int(map_range(z, -15, -20, 100, 65535))
    # print(new_x, new_y, new_z)
    
    t_x = int(map_range(new_x, 0, 65520, 0, 8))
    if t_x > 7: t_x = 7
    t_y = int(map_range(new_y, 0, 65520, 0, 4))
    if t_y > 3: t_y = 3
    t_z = int(new_z)
    # print(t_x, t_y, t_z)
    trellis.pixels[t_x, t_y] = (t_z)
    
    # print(new_x, new_y)
    pitch_dac.value = new_x
    gate_dac.value = new_y
    time.sleep(step_delay)
    
    trellis.pixels[t_x, t_y] = (0)