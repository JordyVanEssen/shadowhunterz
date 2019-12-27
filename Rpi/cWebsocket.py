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

color = [0, 255, 0]
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
            print(incomingData)

            data = json.loads(incomingData)

            if data['mode'] == "Config":
                fileWriter = FileWriter()
                fileWriter.writeToFile('config.json', json.dumps(data, indent=4, sort_keys=True))

            if data['mode'] == "Color":
                busy = True
                color[0] = data['R']
                color[1] = data['G']
                color[2] = data['B']
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
                defaultFunctions = ['rainbow', 'rainbowCycle', 'theaterChase', 'theatherRainbowChase', 'draw', 'colorWipe', 'sensor', 'wave']
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

def getColor():
    global busy, color

    if not busy:
        return color

def getIp():
    ip = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

async def wsSend(msg):
    global ws
    await ws.send(json.dumps(msg))

def run():
    try:
        asyncio.set_event_loop(asyncio.new_event_loop())
        start_server = websockets.serve(readIncomingData, getIp(), 8765)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        asyncio.get_event_loop().stop()
    finally:
        asyncio.get_event_loop().stop()