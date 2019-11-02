#!/usr/bin/env python

# WS server example
from cFileWriter import FileWriter

import asyncio
import websockets
import json


color = [0, 255, 0]
busy = False
function = 'draw'

async def readIncomingData(websocket, path):
    global color, busy, function
    busy = True
    incomingData = { 
            "mode":""
        }
    incomingData = await websocket.recv()
    print(incomingData)
    data = json.loads(incomingData)

    if data['mode'] == "Config":
        fileWriter = FileWriter()
        fileWriter.writeToFile(json.dumps(data, indent=4, sort_keys=True))
    if data['mode'] == "Color":
        color[0] = data['R']
        color[1] = data['G']
        color[2] = data['B']
    if data['mode'] == "sensor":
        pass
    if data['mode'] == "function":
        function = data['function']

    busy = False

def returnFunc():
    return function

def getColor():
    global busy, color

    if not busy:
        return color


def run():
    asyncio.set_event_loop(asyncio.new_event_loop())
    start_server = websockets.serve(readIncomingData, "172.19.3.121", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()