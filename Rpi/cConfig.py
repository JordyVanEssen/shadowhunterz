class LedstripConfig:
    
    def __init__(self, ledX, ledY, squareX, squareY, brightness, ledCount):
        # if yout want to change these remotily just add a parameter and assign it to the correct variable
        # LED strip configuration:
        self.ledPin        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
        self.ledFreqHz    = 800000  # LED signal frequency in hertz (usually 800khz)
        self.ledDma      = 10      # DMA channel to use for generating signal (try 10)
        self.ledInvert     = False   # True to invert the signal (when using NPN transistor level shift)
        self.ledChannel    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

        self.brightness = brightness
        self.ledCount = ledCount

        # set by parameters -> can be remotily changed -> websocket
        self.ledX = ledX
        self.ledY = ledY
        self.squareX = squareX
        self.squareY = squareY
