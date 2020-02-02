from cFileWriter import FileWriter
from cCreateCustomFunctions import createFunctions
from CustomFunctions.cControl import control

import asyncio
import websockets
import json
import os
import socket
import urllib
import smtplib

arduinoColor = [255, 0, 0]
websiteColor = [255, 0, 0]
color = [255, 0, 0]

busy = False
function = 'draw'
ws = None

async def readIncomingData(websocket, path):
    global ws
    ws = websocket
    while True:
        try:
            global color, busy, function
            incomingData = { 
                    "mode":""
                }
            incomingData = await websocket.recv()

            data = json.loads(incomingData)
            print(incomingData)
            if data['mode'] == "Config":
                fileWriter = FileWriter()
                fileWriter.writeToFile('config.json', json.dumps(data, indent=4, sort_keys=True))

            if data['mode'] == "Color":
                busy = True
                websiteColor[0] = data['R']
                websiteColor[1] = data['G']
                websiteColor[2] = data['B']
                busy = False

            if data['mode'] == "sensor":
                pass

            if data['mode'] == "function":
                function = data['function']

            if data['mode'] == "file":
                customFunction = createFunctions(data['name'])
                customFunction.addNewFunction(data['customFunction'])

            if data['mode'] == "getAll":
                getFunction = control()
                defaultFunctions = ['rainbow', 'rainbowCycle', 'theaterChase', 'theatherRainbowChase', 'draw', 'WhacMole', 'clearPanel']
                customFunctions = getFunction.getAll()
                
                for f in defaultFunctions:
                    customFunctions.append(f)

                jsonMessage = {
                    "mode":"availableFunctions",
                    "functions": customFunctions
                }
                await wsSend(jsonMessage)

        except websockets.ConnectionClosed:
            pass

def returnFunc():
    global function
    return function

def setFunction(f):
    global function
    function = f

def getColor():
    return compareColor()

def compareColor():
    global arduinoColor, websiteColor, color
    inRange = True
    if (color[0]) > (arduinoColor[0] + 5) or (color[1]) > (arduinoColor[1] + 5) or (color[2] > (arduinoColor[2] + 5)):
        inRange = False

    if (color[0]) < (arduinoColor[0] - 5) or (color[1]) < (arduinoColor[1] - 5) or (color[2] < (arduinoColor[2] - 5)):
        inRange = False
    
    if (inRange) and (color != websiteColor):
        #color = websiteColor
        pass
    else:
        color = arduinoColor

    return color


def getIp():
    ip = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    print(ip)
    return ip

def setColor(c):
    global arduinoColor
    arduinoColor = c

async def wsSend(msg):
    global ws
    await ws.send(json.dumps(msg))

def run():
    try:
        print("websocket thread running")
        asyncio.set_event_loop(asyncio.new_event_loop())
        start_server = websockets.serve(readIncomingData, getIp(), 8765)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        asyncio.get_event_loop().stop()
    finally:
        asyncio.get_event_loop().stop()