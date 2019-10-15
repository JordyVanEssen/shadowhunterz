# Raspberry Pi to Arduino I2C Communication 
# Python Code 
 
import smbus
import time 
from neopixel import *
import argparse
import random

# Slave Addresses for Arduinos 
ARDUINO_1_ADDRESS = 0x04 # I2C Address of Arduino 1 


# LED strip configuration:
LED_COUNT      = 64      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

X_MAX = 8
Y_MAX = 8

SQUARE_X = 4
SQUARE_Y = 4

# 2d array for the sqaures which are lit up
# stores the exact id of the sensor/square
# the arduino sends his panel location and the sensor id
# so the rpi knows which sqaure to light up

# store the number of the first LED of the square
# turns ON if its not in the array 
# if it is pressent in the array, turn it off
litUpSquare = [ ]

# Create the I2C bus 
bus = smbus.SMBus(1) 
on = False

#----------------------------------

# CLASSES #

class Coordinate:
  def __init__(self, x, y):
    self.x = x
    self.y = y

# FUNCTIONS #

 # This function converts a string to an array of bytes. 
def ConvertStringToBytes(src):
  try:
    bus.write_byte_data(ARDUINO_1_ADDRESS, 0x00, ord(src))
    print("Sent: %d" %ord(src))
  except:
    print("Error occured in the sending")


def readInput():
  try:
    data = bus.read_byte(ARDUINO_1_ADDRESS)
    if data > 0:
      print("received: %d" %data)
      if data not in litUpSquare:
        litUpSquare.append(data)
      else:
        litUpSquare.remove(data)
    return data or -1
  except:
    print("Error occured in reading")


def calculateLeds(x, y):
    y += 1
    if y % 2 != 0:
        return (x + ((y - 1) * X_MAX))
    else:
        return ((((y - 1) * X_MAX)) + (X_MAX - x)) - 1


def drawSquare(strip, ledArray, color):
    for led in ledArray:
        strip.setPixelColor(led - 1, color)
        strip.show()

def fillBoard(strip):
    for y in range(0, Y_MAX, 2):
        for x in range(0, X_MAX, 2):
            drawSquare(strip, x, y, 2, Color(0, 255, 0))
            time.sleep(500/1000)

def sensorCoordToLedCoord(x, y):
    return (y * Y_MAX + x)


def calculateSensorCoord(sensorId):
    sensorId -= 1
    rest = sensorId
    yresult = 0

    for i in range(SQUARE_Y):
        if rest >= SQUARE_X:
            rest -= SQUARE_Y
            yresult += 1
    
    return Coordinate(rest+1, yresult+1)

def calcLEDS(num, x):
    x1 = num
    x2 = num + 1
    x3 = num + (((2*X_MAX)-1) - ((x-1)*4))-1
    x4 = x3 + 1
    arr = {x1, x2, x3, x4}
    print(arr)
    return arr

def calcTopLeftSquare(x, y):
    return x * 2 - 1 + (((y*2-1)-1) * Y_MAX)

def testLed(strip):
    for y in range(Y_MAX):
        for x in range(X_MAX):
            strip.setPixelColor(calculateLeds(y,  x), Color(0, 255, 0))
            strip.show()
            print(x, " ", y)


if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    #fillBoard(strip)
    coordinate = None

    while True:
        time.sleep(0.1)

        sensId = readInput()

        if sensId >= 0:
            coordinate = calculateSensorCoord(sensId)

        color = Color(0, 0, 0)

        if sensId in litUpSquare:
            color = Color(0, 255, 0)

        if coordinate is not None:
            drawSquare(strip, calcLEDS(calcTopLeftSquare(coordinate.x, coordinate.y), coordinate.x), 2, color)
            coordinate = None

    for i in range(1, 17):
        coordinate = calculateSensorCoord(i)
        print('\n\nx:', coordinate.x, 'y: ', coordinate.y)
        print(coordinate.x * 2 - 1 + (((coordinate.y*2-1)-1) * Y_MAX))
        drawSquare(strip, calcLEDS(calcTopLeftSquare(coordinate.x, coordinate.y), coordinate.x), Color(255, 0, 0))
        time.sleep(500/1000)



