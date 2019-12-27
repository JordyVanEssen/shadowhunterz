from cLedFunctions import LedFunctions
from CustomFunctions.cControl import control
from cWebsocket import getColor, returnFunc, wsSend
from neopixel import *

import os
import time 
import argparse
import importlib
import asyncio
import json

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
        function = returnFunc()

        if currentMode != function:
            if function == 'colorWipe':
                customColor = getColor()
                # GRB
                color = Color(int(customColor[1]), int(customColor[0]), int(customColor[2]))
                panelFunctions.colorWipe(color)
            else:
                if control.ifMethodExist(function) is True:
                    error = False
                    path = '{homeDir}/CustomFunctions/f_{fileName}.py'.format(homeDir=os.getcwd(), fileName=function)
                    f = open(path, 'r')
                    code_str = f.read()
                    try:
                        method = compile(code_str, "{fName}.py".format(fName=function), 'exec')
                        while(returnFunc() == currentMode) and not error:
                            exec(method)
                    except Exception as e:
                        error = True
                        jsonMessage = {
                            "mode":"error",
                            "message": str(e)
                        }
                        print(jsonMessage)
                        loop = asyncio.get_event_loop()
                        loop.run_until_complete(wsSend(jsonMessage))
                    
                else:
                    getattr(panelFunctions, function)()
                
            

except KeyboardInterrupt:
    if args.clear:
        panelFunctions.colorWipe(Color(0, 0, 0), 10)

