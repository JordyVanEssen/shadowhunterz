from cLedFunctions import LedFunctions
import time 
import argparse
from cWebsocket import getColor
from neopixel import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    panelFunctions = LedFunctions()

    currentMode = ''

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

try:
    while True:
        function = panelFunctions.getFunc()

        if currentMode != function:
            panelFunctions.colorWipe(Color(0, 0, 0))

            if function == 'draw':
                panelFunctions.draw()
            elif function == 'rainbow':
                panelFunctions.rainbow()
            elif function == 'colorWipe':
                customColor = getColor()
                color = Color(int(customColor[1]), int(customColor[0]), int(customColor[2]))
                panelFunctions.colorWipe(color)
            elif function == 'theaterChase':
                panelFunctions.theaterChase()
            elif function == 'theaterChaseRainbow':
                panelFunctions.theaterChaseRainbow()
            elif function == 'rainbowCycle':
                panelFunctions.rainbowCycle()
            elif function == '':
                pass

except KeyboardInterrupt:
    if args.clear:
        panelFunctions.colorWipe(Color(0, 0, 0), 10)

