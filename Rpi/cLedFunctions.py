from cCalculations import Calculations
from cArduinoCommunication import I2Csetup
from cFileWriter import FileWriter
from cConfig import LedstripConfig
from cWebsocket import getColor, run, returnFunc, setColor
from cIOcontroller import IOcontroller
from neopixel import *
from PIL import Image 
from os import listdir
from os.path import isfile, join
import random
import threading
import time
import json

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

    # Whac-A-Mole score and speed
    score = 0
    speed = 5.0

    # control the io pins
    controller = IOcontroller()

    def __init__(self):
        self.configurePanel()
        self.setupStrip()
        i = 0
        for i in range(self.config.panels * 3):
            print(i + 4)
            self.arduinoAdresses.append(i + 4)

    # -- asks every arduino if an IR-sensor was activated
    # -- probably need to put every panel in a thread...
    def readInput(self):
        for i in range(len(self.arduinoAdresses)):
            sensId = self.i2cBus.readInput(self.arduinoAdresses[i])
            if sensId is not None:
                if sensId >= 1:
                    return sensId
        return None

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

        sensId = self.readInput()

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
        """ drawing mode """
        coordinate = None

        time.sleep(0.1)

        sensId = self.readInput()
        
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
        if self.score >= 1:
            self.speed *= 0.965
            if float(self.speed) < 0.75:
                self.speed = 0.75

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
        print(float(self.speed))

        current = time.time()
        while True:
            if returnFunc() != "WhacMole":
                return
            sensId = self.readInput()

            elapsed = time.time() - current
            if elapsed < float(self.speed):
                if sensId is not None: 
                    if sensId >= 1:
                        if sensId == randomSquare:
                            self.score += 1 
                            coordinate = self.calculate.calculateSensorCoord(randomSquare)
                            self.drawSquare(self.calculate.calcLEDS(self.calculate.calcTopLeftSquare(coordinate.x, coordinate.y), coordinate.x), [0, 0, 0])
                            if self.score >= 99:
                                self.endGame(Color(255, 0, 0))
                            break
            elif elapsed > float(self.speed):
                self.endGame(Color(0, 255, 0))

    def endGame(self, c):
        """         for x in range(3):  
        color = c
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()
        time.sleep(1)
        color = Color(0, 0, 0)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()
        time.sleep(1)  """
        self.clearPanel()
        self.showScore(self.score, 2, 0, 5)
        self.showHighscore(self.score)
        self.clearPanel()
        self.score = 0
        self.time = 5.0
        setFunction("draw")

    # show the score
    def showScore(self, score, offsetX, offsetY, d):
        # left and right number
        l = 0
        r = 0
        x = list(str(score))
        if score > 9:
            l = x[0]
            r = x[1]
        else:
            r = x[0]

        # default color
        color = [0, 0, 255]

        """self.showImage(0, 'numbers/L' + str(l) + '.png', False)
        self.showImage(0, 'numbers/R' + str(r) + '.png', False)
        time.sleep(5) """

        numL = Image.open(r'numbers/L' + str(l) + '.png')
        numR = Image.open(r'numbers/R' + str(r) + '.png')

        pixelsL = list(numL.getdata())
        pixelsR = list(numR.getdata())

        width, height = numL.size
        pixelsL = [pixelsL[i * width:(i + 1) * width] for i in range(height)]
        pixelsR = [pixelsR[i * width:(i + 1) * width] for i in range(height)]

        for y in range(12):
            for x in range(12):
                if pixelsL[y][x][0] == 255:
                    self.drawSquare(self.calculate.calcLEDS(self.calculate.calcTopLeftSquare(x, y + offsetY), x), color)

        for y in range(12):
            for x in range(12):
                if pixelsR[y][x][0] == 255:
                    self.drawSquare(self.calculate.calcLEDS(self.calculate.calcTopLeftSquare(x + offsetX, y + offsetY), x + offsetX), color)
       
        time.sleep(5)
    
    # shows the highscore
    def showHighscore(self, score):
        self.clearPanel()
        print("showing highscore")
        with open('highscore.json') as json_file:
            data = json.load(json_file)

        highscore = int(data["highscore"])
        print(highscore)
        print(score)

        if score > highscore:
            highscore = score
            newHighscore =  {
                "highscore": score
            }
            with open('highscore.json', 'w', encoding='utf-8') as f:
                json.dump(newHighscore, f, ensure_ascii=False, indent=4)

        self.showNumber('numbers/HS.png')


        self.showScore(highscore, 2, 3, 4)
        print("done highscore")
    
    def showNumber(self, path):
        nm = Image.open(path, 'r')
        pixels = list(nm.getdata())
        width, height = nm.size
        pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
        for y in range(12):
            for x in range(12):
                if pixels[y][x][0] == 255:
                    self.drawSquare(self.calculate.calcLEDS(self.calculate.calcTopLeftSquare(x + 1, y + 1), x + 1), [0, 0, 255])
    
    #shows images
    def showImage(self, d, frame, resize):
        print(frame)
        pixels = self.getImagePixels(frame, resize)
        for i in range(24):
            for j in range(24):
                self.strip.setPixelColor(self.calculate.calculateLeds(j, i), Color(int(float(pixels[i][j][1]) * 0.3), int(float(pixels[i][j][0]) * 0.3), int(float(pixels[i][j][2]) * 0.3)))
        self.strip.show()
        time.sleep(d)
    
    # gets all the pixel values from the given image
    def getImagePixels(self, path, resize):
        imageRatio = 24
        im = Image.open(path, 'r')
        if resize:
            im = im.resize((int(imageRatio), int(imageRatio)), resample=Image.BILINEAR)

        pixels = list(im.getdata())
        width, height = im.size
        pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
        return pixels

    # shows all the images in a 
    def showGif(self):
        gif = "pacman"
        path =  'images/gifs/'
        finalPath = path + gif 
        frames =  [f for f in listdir(finalPath) if isfile(join(finalPath, f))]
        size = len(frames)
        for i in range(int(size)):
            self.showImage(1, finalPath + "/" + gif + str(i) + ".jpg", True)