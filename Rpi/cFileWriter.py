import json

busy = False

class FileWriter():
    def __init__(self):
        pass

    def writeToFile(self, data):
        global busy
        busy = True
        f = open('config.json', 'w+')
        f.write(data)
        f.close()
        busy = False

    def readFile(self):
        global busy
        if not busy:
            with open('config.json', 'r') as file:
                data = json.load(file)
                return data