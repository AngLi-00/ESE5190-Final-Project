# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time
import busio
import board
import math
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
import adafruit_character_lcd.character_lcd_i2c as character_lcd

i2c_2 = busio.I2C(board.SCL, board.SDA)
#i2c = board.STEMMA_I2C()  # uses board.SCL and board.SDA
i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = LSM6DSOX(i2c, 0x6b)
lcd_columns = 16
lcd_rows = 2
lcd = character_lcd.Character_LCD_I2C(i2c_2, lcd_columns, lcd_rows)
# Print a two line message

while True:

    acc_x, acc_y, acc_z = sensor.acceleration


    angle_x = (math.atan(acc_x / (math.sqrt(acc_y * acc_y + acc_z * acc_z)))) * 180.0 / math.pi
    angle_y = (math.atan(acc_y / (math.sqrt(acc_x * acc_x + acc_z * acc_z)))) * 180.0 / math.pi
    angle_z = (math.atan(acc_z / (math.sqrt(acc_x * acc_x + acc_y * acc_y)))) * 180.0 / math.pi

    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (sensor.acceleration))
    print("Move Angle: X: {0}, Y = {1}, Z = {2}".format(angle_x, angle_y, angle_z))
    if angle_y < 55:
        lcd.backlight = True
        lcd.clear()
        lcd.message = "PLS Correct your \nposture "
        print("Please correct your sitting posture.")
    else:
        lcd.clear()
    print("")
    time.sleep(0.5)
