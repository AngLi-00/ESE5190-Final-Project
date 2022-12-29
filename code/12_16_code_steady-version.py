import time
import busio
import board
import analogio
import digitalio
import math
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
import adafruit_character_lcd.character_lcd_i2c as character_lcd
import adafruit_hcsr04
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
import random


sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.A0, echo_pin=board.A1)
i2c_2 = busio.I2C(board.SCL, board.SDA)
i2c = board.STEMMA_I2C()  
sensor = LSM6DSOX(i2c, 0x6b)
lcd_columns = 16
lcd_rows = 2
lcd = character_lcd.Character_LCD_I2C(i2c_2, lcd_columns, lcd_rows)

time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)
str = input("Please choose the mode.\nType in 0 for 'Posture Helper', 1 for 'Joystick':")


if str == '0':  #"Posture Helper"
    print ("You choose the 'Posture Helper' mode", str)

    while True:
        acc_x, acc_y, acc_z = sensor.acceleration
        
        angle_x = (math.atan(acc_x / (math.sqrt(acc_y * acc_y + acc_z * acc_z)))) * 180.0 / math.pi
        angle_y = (math.atan(acc_y / (math.sqrt(acc_x * acc_x + acc_z * acc_z)))) * 180.0 / math.pi
        angle_z = (math.atan(acc_z / (math.sqrt(acc_x * acc_x + acc_y * acc_y)))) * 180.0 / math.pi

        print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (sensor.acceleration))
        print("Move Angle: X: {0}, Y = {1}, Z = {2}".format(angle_x, abs(angle_y), angle_z))

        lcd.clear()

        try:
            print((sonar.distance))
            if abs(angle_y) < 65  and sonar.distance > 40: #ANGLE LIMIT MAY REPLACED BY 47
                lcd.message = "PLS Correct your \nposture "
                print("Please correct your sitting posture!")
                mouse.move(x=10)#Mouse shake!
                mouse.move(y=10)
                mouse.move(x=-10)
                mouse.move(y=-10)
            elif abs(angle_y) > 65  and sonar.distance < 40:
                print("You are too close to the screen!")
                lcd.message = "Too close to\nthe screen!"
                mouse.move(x=10)
                mouse.move(y=10)
                mouse.move(x=-10)
                mouse.move(y=-10)
            elif abs(angle_y) < 65  and sonar.distance < 40:
                print("Away from screen! Sit up straight")
                lcd.message = "Away from screen\nSit up straight"
                mouse.move(x=10)
                mouse.move(y=10)
                mouse.move(x=-10)
                mouse.move(y=-10)
            else:
                pass
            time.sleep(0.3)
        except RuntimeError:
            print("Retrying!")
            lcd.message = "PLS face the scr\nsensor not work"
            time.sleep(0.3)
  
elif str == '1':  #"Joystick"
    print ("You choose the 'Joystick' mode", str)
    while True:
        acc_x, acc_y, acc_z = sensor.acceleration
        
        angle_x = (math.atan(acc_x / (math.sqrt(acc_y * acc_y + acc_z * acc_z)))) * 180.0 / math.pi
        angle_y = (math.atan(acc_y / (math.sqrt(acc_x * acc_x + acc_z * acc_z)))) * 180.0 / math.pi
        angle_z = (math.atan(acc_z / (math.sqrt(acc_x * acc_x + acc_y * acc_y)))) * 180.0 / math.pi

        print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (sensor.acceleration))
        print("Move Angle: X: {0}, Y = {1}, Z = {2}".format(angle_x, angle_y, angle_z))

        if angle_z>40:
            print("up")
            keyboard.press(82)
            keyboard.release_all()
        elif angle_z<0:
            print("down")
            keyboard.press(81)
            keyboard.release_all()
        elif angle_x<-18:
            print("left")
            keyboard.press(80)
            keyboard.release_all()
        elif angle_x>22:
            print("right")
            keyboard.press(79)
            keyboard.release_all()
        elif angle_z<40 and angle_z>32:
            print("slow up")
            keyboard.press(82)
            keyboard.release_all()
            time.sleep(0.05)
        elif angle_z<8 and angle_z>0:
            print("slow down")
            keyboard.press(81)
            keyboard.release_all()
            time.sleep(0.05)
        elif angle_x<-10 and angle_x>-18:
            print("slow left")
            keyboard.press(80)
            keyboard.release_all()
            time.sleep(0.05)
        elif angle_x<22 and angle_x>14:
            print("slow right")
            keyboard.press(79)
            keyboard.release_all()
            time.sleep(0.05)


else:
    print("Input error！")