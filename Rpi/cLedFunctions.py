from cCalculations import Calculations
from cArduinoCommunication import I2Csetup
from cFileWriter import FileWriter
from cConfig import LedstripConfig
from cWebsocket import getColor, run, returnFunc, setColor
from cIOcontroller import IOcontroller
from neopixel import *
from PIL import Image 
import random
import threading
import time

class LedFunctions:
    # the ledstrip
    strip = None
    
    # the leds on the x and y axis 
    X_MAX = 0
    Y_MAX = 0
    SQUARE_X = 0
    SQUARE_Y = 0
    arduinoAdresses = [ ]

    # calculations are found in this class: Calculations
    calculate = None

    config = None
 
    mode = 'draw'
    # store the number of the SensorId of the square
    # turns ON if its not in the array 
    # if it is pressent in the array, turn it off
    litUpSquare = [ ]

    # the i2c bus, used to communicate with the arduino's
    i2cBus = I2Csetup(0x05)

    # Whac-A-Mole score
    score = 0

    # control the io pins
    controller = IOcontroller()

    def __init__(self):
        print('ledfunctions available...')
        self.configurePanel()
        self.setupStrip()
        i = 0
        for i in range(self.config.panels * 3):
            self.arduinoAdresses.append(i + 4)
            print(self.arduinoAdresses[i])

    # -- asks every arduino if an IR-sensor was activated
    # -- probably need to put every panel in a thread...
    def readInput(self, address):
        #i2cBus = I2Csetup(address)
        return self.i2cBus.readInput(address)

    # -- configure the panel and strip
    def configurePanel(self):
        fileWriter = FileWriter()
        config = fileWriter.readFile('config.json')

        self.config = LedstripConfig(int(config['ledX']), int(config['ledY']), int(config['squareX']), int(config['squareY']), int(config['brightness']), int(config['ledCount']), int(config['panels']))
        self.calculate = Calculations(self.config.ledX, self.config.ledY, self.config.squareX, self.config.squareY)

    def setupStrip(self):
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(self.config.ledCount, self.config.ledPin, self.config.ledFreqHz, self.config.ledDma, self.config.ledInvert, self.config.brightness, self.config.ledChannel)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    def getStrip(self):
        return self.strip

    def drawSquare(self, ledArray, color):
        if len(ledArray) > 1:
            for led in ledArray:
                self.strip.setPixelColor(led - 1, Color(int(color[1]), int(color[0]), int(color[2])))
            self.strip.show()

    def theaterChase(self, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        customColor = getColor()
        color = Color(int(customColor[1]), int(customColor[0]), int(customColor[2]))
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, color)
                self.strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, 0)

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                if returnFunc() != "rainbow":
                    return
                self.strip.setPixelColor(i, self.wheel((i + j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def rainbowCycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, self.wheel((i+j) % 255))
                self.strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, 0)
    
    def wave(self):
        """Leds turn off in the order they turned on."""
        previousMillis = 0
        interval = 2
        milli_sec = time.time()
        coordinate = None

        for i in range(len(self.arduinoAdresses)):
            sensId = self.readInput(self.arduinoAdresses[i])
            if sensId is not None:
                break

        if sensId is not None:
            if sensId >= 1:
                milli_sec = time.time()
                if sensId not in self.litUpSquare:
                    self.litUpSquare.append(sensId)
        
        if sensId >= 1:
            coordinate = self.calculate.calculateSensorCoord(sensId)

        color = Color(0, 255, 0)

        if sensId in self.litUpSquare:
            customColor = getColor()
            # it uses GRB instead of RGB
            color = Color(int(customColor[1]), int(customColor[0]), int(customColor[2]))

        if coordinate is not None:
            self.drawSquare(self.calculate.calcLEDS(self.calculate.calcTopLeftSquare(coordinate.x, coordinate.y), coordinate.x), color)
            coordinate = None

        if time.time() - milli_sec > interval:
            milli_sec = time.time()

            for i in range(len(self.litUpSquare)):
                coordinate = self.calculate.calculateSensorCoord(self.litUpSquare[i])
                self.drawSquare(self.calculate.calcLEDS(self.calculate.calcTopLeftSquare(coordinate.x, coordinate.y), coordinate.x), Color(0, 0, 0))
                time.sleep(1.5)
            self.litUpSquare.clear()


    def draw(self):
        coordinate = None

        time.sleep(0.1)

        for i in range(len(self.arduinoAdresses)):
            sensId = self.readInput(self.arduinoAdresses[i])
            if sensId is not None:
                if sensId >= 1:
                    break
        
        if sensId is not None:
            if sensId >= 1:
                if sensId not in self.litUpSquare:
                    self.litUpSquare.append(sensId)

            if sensId >= 1:
                coordinate = self.calculate.calculateSensorCoord(sensId)

            color = [0, 0, 0]
            if self.controller.getMode() is 1:
                if sensId in self.litUpSquare:
                    self.controller.getColorFromArduino()
                    customColor = getColor()

                    # it uses GRB instead of RGB
                    color = customColor
                    #color = Color(int(customColor[1]), int(customColor[0]), int(customColor[2]))
            elif self.controller.getMode() is 0:
                self.litUpSquare.remove(sensId)

            if coordinate is not None:
                self.drawSquare(self.calculate.calcLEDS(self.calculate.calcTopLeftSquare(coordinate.x, coordinate.y), coordinate.x), color)
                coordinate = None

    def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)
    
    def clearPanel(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0,0,0))
        self.strip.show()

    def WhacMole(self):
        """ Whaca-A-Mole Game."""
        Red = 0
        Green = 0
        Blue = 0
        
        x = self.score / 5
        if x >= 1 and x < 2:
            Green = 255
        elif x >= 2 and x < 3:
            Green = 255
            Red = 255
        elif x >= 3 and x < 4:
            Green = 200 
            Red = 255
        elif x >= 4 and x < 5:
            Green = 120
            Red = 255
        elif x >= 5:
            Green = 20
            Red = 255
        else:
            Green = 160

        color = [Red, Green, Blue]

        randomSquare = random.randrange(1, self.config.squareX * self.config.squareY + 1)
        coordinate = self.calculate.calculateSensorCoord(randomSquare)
        
        self.drawSquare(self.calculate.calcLEDS(self.calculate.calcTopLeftSquare(coordinate.x, coordinate.y), coordinate.x), color)

        current = time.time()
        while True:
            if returnFunc() != "WhacMole":
                return
            for i in range(len(self.arduinoAdresses)):
                sensId = self.readInput(self.arduinoAdresses[i])
                if sensId is not None:
                    if sensId >= 1:
                        break

            elapsed = time.time() - current
            if elapsed < 5:
                if sensId is not None: 
                    if sensId >= 1:
                        if sensId == randomSquare:
                            self.score += 1 
                            coordinate = self.calculate.calculateSensorCoord(randomSquare)
                            self.drawSquare(self.calculate.calcLEDS(self.calculate.calcTopLeftSquare(coordinate.x, coordinate.y), coordinate.x), [0, 0, 0])
                            break
            elif elapsed > 5:
                self.score = 0
                for i in range(5):  
                    color = Color(0,255,0) 
                    for i in range(self.strip.numPixels()):
                        self.strip.setPixelColor(i, color)
                    self.strip.show()
                    time.sleep(1)
                    color = Color(0, 0, 0)
                    for i in range(self.strip.numPixels()):
                        self.strip.setPixelColor(i, color)
                    self.strip.show()
                    time.sleep(1)
                break


"""     def showScore(self):
        x = map(int, str(self.score))
            
        l = x[0]
        r = x[1]
        color = Color(255,0,0)

        numL = Image.open('numbers\L' + str(l) + '.png')
        numR = Image.open('numbers\R' + str(r) + '.png')

        pixelsL = list(numL.getdata())
        pixelsR = list(numR.getdata())

        width, height = numL.size

        pixelsL = [pixelsL[i * width:(i + 1) * width] for i in xrange(height)]
        pixelsR = [pixelsR[i * width:(i + 1) * width] for i in xrange(height)]

        for y in range(12):
            for x in range(12):
                if pixelsL[y][x][0] == 255:
                    self.drawSquare(self.calculate.calcLEDS(self.calculate.calcTopLeftSquare(x, y), x), color)

        for y in range(12):
            for x in range(12):
                if pixelsR[y][x][0] == 255:
                    self.drawSquare(self.calculate.calcLEDS(self.calculate.calcTopLeftSquare(x, y), x), color) """
