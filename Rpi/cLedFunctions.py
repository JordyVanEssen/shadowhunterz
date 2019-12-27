from cCalculations import Calculations
from cArduinoCommunication import I2Csetup
from cFileWriter import FileWriter
from cConfig import LedstripConfig
from cWebsocket import getColor, run, returnFunc
from neopixel import *
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
    # -- the amount of panels on the wall
    panels = 1
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
    i2cBus = I2Csetup(0x04)

    def __init__(self):
        print('ledfunctions available...')
        self.configurePanel()
        self.setupStrip()
        i = 0
        for i in range(self.panels * 3):
            self.arduinoAdresses.append(hex(i + 3))

    # -- asks every arduino if an IR-sensor was activated
    # -- probably need to put every panel in a thread...
    def readInput(self, address):
        return self.i2cBus.readInput(address)

    def startThread(self):
        thread = threading.Thread(target=run)
        thread.start()

    # -- configure the panel and strip
    def configurePanel(self):
        fileWriter = FileWriter()
        config = fileWriter.readFile('config.json')
        

        self.config = LedstripConfig(int(config['ledX']), int(config['ledY']), int(config['squareX']), int(config['squareY']), int(config['brightness']), int(config['ledCount']))
        self.calculate = Calculations(self.config.ledX, self.config.ledY, self.config.squareX, self.config.squareY)

    def setupStrip(self):
        print(str(self.config))
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(self.config.ledCount, self.config.ledPin, self.config.ledFreqHz, self.config.ledDma, self.config.ledInvert, self.config.brightness, self.config.ledChannel)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
    # -- end config strip/panels

    def getStrip(self):
        return self.strip

    def drawSquare(self, ledArray, color):
        print("drawing square")
        print(color)
        if len(ledArray) > 1:
            for led in ledArray:
                self.strip.setPixelColor(led - 1, color)
                self.strip.show()

    def fillBoard(self):
        for y in range(0, self.Y_MAX, 2):
            for x in range(0, self.X_MAX, 2):
                drawSquare(strip, x, y, 2, Color(0, 255, 0))
                time.sleep(500/1000)
    
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
                self.strip.setPixelColor(i, self.wheel((i+j) & 255))
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

        i = 0
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

        color = Color(0, 0, 0)

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

        """ i = 0
        for i in range(len(self.arduinoAdresses)):
            sensId = self.readInput(self.arduinoAdresses[i])
            if sensId is not None:
                break """
        sensId = self.readInput(0x04)

        if sensId is not None:
            if sensId >= 1:
                if sensId not in self.litUpSquare:
                    self.litUpSquare.append(sensId)
                else:
                    self.litUpSquare.remove(sensId)

            if sensId >= 1:
                coordinate = self.calculate.calculateSensorCoord(sensId)

            color = Color(0, 0, 0)
            if sensId in self.litUpSquare:
                customColor = getColor()
                # it uses GRB instead of RGB
                color = Color(int(customColor[1]), int(customColor[0]), int(customColor[2]))

            if coordinate is not None:
                self.drawSquare(self.calculate.calcLEDS(self.calculate.calcTopLeftSquare(coordinate.x, coordinate.y), coordinate.x), color)
                coordinate = None
                
                

    def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def turnOn(self, id):
        self.strip.setPixelColor(id, Color(0,255,0))
        self.strip.show()