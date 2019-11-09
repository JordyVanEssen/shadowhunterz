from cLedFunctions import LedFunctions
from CustomFunctions.cControl import control
from cWebsocket import getColor
from neopixel import *

import os
import time 
import argparse
import importlib

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    panelFunctions = LedFunctions()
    panelFunctions.startThread()

    currentMode = ''

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

try:
    control = control()
    while True:
        function = panelFunctions.getFunc()

        if currentMode != function:
            panelFunctions.colorWipe(Color(0, 0, 0))
            
            if function == 'colorWipe':
                customColor = getColor()
                # GRB
                color = Color(int(customColor[1]), int(customColor[0]), int(customColor[2]))
                panelFunctions.colorWipe(color)
            else:
                if control.ifMethodExist(function) is True:
                    path = '{homeDir}/CustomFunctions/f_{fileName}.py'.format(homeDir=os.getcwd(), fileName=function)
                    f = open(path, 'r')
                    code_str = f.read()
                    method = compile(code_str, "{fName}.py".format(fName=function), 'exec')
                    exec(method)
                else:
                    getattr(panelFunctions, function)()
                
            

except KeyboardInterrupt:
    if args.clear:
        panelFunctions.colorWipe(Color(0, 0, 0), 10)

