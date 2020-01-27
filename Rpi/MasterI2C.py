from cLedFunctions import LedFunctions
from CustomFunctions.cControl import control
from cWebsocket import getColor, returnFunc, wsSend, setFunction, run, getIp
from cIOcontroller import IOcontroller
from neopixel import *

import os
import time 
import argparse
import importlib
import asyncio
import json
import threading

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    panelFunctions = LedFunctions()
    threading.Thread(target = run).start()

    controller = IOcontroller()
    controller.startThread()
    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

try:
    control = control()
    #controller.startThread()
    currentMode = ''

    while True:
        #controller.getColorFromArduino()
        function = returnFunc()
        if currentMode != function:
            #currentMode = function
            if function == 'colorWipe':
                controller.getColorFromArduino()
                customColor = getColor()
                # GRB
                color = Color(int(customColor[1]), int(customColor[0]), int(customColor[2]))
                panelFunctions.colorWipe(color)
            else:
                if control.ifMethodExist(function) is True:
                    path = '{homeDir}/CustomFunctions/f_{fileName}.py'.format(homeDir=os.getcwd(), fileName=function)
                    f = open(path, 'r')
                    code_str = f.read()
                    try:
                        method = compile(code_str, "{fName}.py".format(fName=function), 'exec')
                        while(returnFunc() == function):
                            exec(method)
                    except Exception as e:
                        sendErrorMessage(str(e))
                else:
                    try:
                        if function == "clearPanel":
                            panelFunctions.clearPanel()
                            setFunction("draw")
                        else:
                            getattr(panelFunctions, function)()

                    except Exception as e:
                        pass
                        #sendErrorMessage(str(e)) 
except KeyboardInterrupt:
    if args.clear:
        panelFunctions.clearPanel()


def sendErrorMessage(msg):
    jsonMessage = {
        "mode":"error",
        "message": msg
    }
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wsSend(jsonMessage))