import json

busy = False

class FileWriter():
    def __init__(self):
        pass

    # overwrites a given file
    def writeToFile(self, path, data):
        global busy
        busy = True
        f = open(path, 'w+')
        f.write(data)
        f.close()
        busy = False

    # reads a given file
    def readFile(self, path):
        global busy
        if not busy:
            with open(path, 'r') as file:
                if path.endswith('.json', len(path) - 5):
                    data = json.load(file)
                elif path.endswith('.txt', len(path) - 4) or path.endswith('.py', len(path) - 3):
                    data = file.read()

                return data

    # adds to a given file
    def addToFile(self, path, data):
        global busy
        if not busy:
            with open(path, 'a') as file:
                file.write(data)
                file.close()
                busy = False