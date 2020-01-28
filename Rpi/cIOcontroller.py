import RPi.GPIO as GPIO
import time
from cArduinoCommunication import I2Csetup
from cWebsocket import setColor, setFunction
import threading


class IOcontroller:

    # initialize the keypad
    KEYPAD = [
        [1],
        [2],
        [3],
        [4]
    ]

    ROW         = [22,23,24,25]
    COLUMN      = [4]

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    # start the thread which monitors the kyepad
    def startThread(self):
        try:
            threading.Thread(target = self.readKeypad).start()
        except expression as identifier:
            pass
    
    # read the keypad and set the function according to the pressed key
    def readKeypad(self):
        print("thread started")
        while True:
            digit = None
            digit = self.getKey()
            if digit is not None:
                if digit is 1:
                    setFunction("clearPanel")
                elif digit is 2:
                    setFunction("rainbowCycle")
                elif digit is 3:
                    setFunction("WhacMole")
                elif digit is 4:
                    setFunction("draw")

    # get the color from the arduino
    def getColorFromArduino(self):
        color = [0, 255, 0]
        bus = I2Csetup(0x03)
        for i in range(3):
            colorInput = bus.readInput(0x03)
            color[i] = colorInput
        setColor(color)

    # get the mode, draw of delete
    def getMode(self): # draw or wipe
	    return GPIO.input(17)

    # gets the pressed key
    def getKey(self):
        # Set all columns as output low
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)

        # Set all rows as input
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Scan rows for pushed key/button
        # A valid key press should set "rowVal"  between 0 and 3.
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = GPIO.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i

        # if rowVal is not 0 thru 3 then no button was pressed and we can exit
        if rowVal <0 or rowVal >3:
            self.exit()
            return

        # Convert columns to input
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Switch the i-th row found from scan to output
        GPIO.setup(self.ROW[rowVal], GPIO.OUT)
        GPIO.output(self.ROW[rowVal], GPIO.HIGH)

        # Scan columns for still-pushed key/button
        # A valid key press should set "colVal"  between 0 and 2.
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = GPIO.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal=j

        # if colVal is not 0 thru 2 then no button was pressed and we can exit
        if colVal <0 or colVal >2:
            self.exit()
            return

        # Return the value of the key pressed
        self.exit()
        return self.KEYPAD[rowVal][colVal]

    
    # on deletion of the object
    def exit(self):
        # Reinitialize all rows and columns as input at exit
        for i in range(len(self.ROW)):
                GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)
