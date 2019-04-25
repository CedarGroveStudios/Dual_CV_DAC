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

# starting and ending note values to map to buttons 0 to 31
start_note = 36
end_note = 67

# CV voltage output
low_out = 960  # for lowest note; actual voltage is 5v*(960/4096) = 1.17v
interval_out = 51.2  # interval value; voltage is 5v*(51.2/4096) = 62.5mv
high_out = low_out + (interval_out * (end_note - start_note + 1))

current_press = set()

while True:
    pressed = set(trellis.pressed_keys)

    for press in pressed - current_press:
        x, y = press
        print("Pressed:", press)
        noteval = start_note + x + (y * 8)
        noteout = int(map_range(noteval, start_note, end_note, low_out, high_out))
        print("noteval = ", noteval, "noteout = ", noteout)  # show note and raw DAC values
        print("output voltage = ", 5 * (noteout / 4096))  # show actual voltage value
        pitch_dac.raw_value = noteout  # set DAC to noteout value (the raw DAC value)
        gate_dac.raw_value = 4095  # set the Gate output to +5 volts
        time.sleep(0.01)

    for release in current_press - pressed:
        x, y = release
        print("Released:", release)
        noteval = start_note + x + (y * 8)
        gate_dac.raw_value = 0  # set the Gate output to 0 volts
        time.sleep(0.01)

    current_press = pressed
