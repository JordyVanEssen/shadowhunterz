from cFileWriter import FileWriter
import os
import json

class createFunctions:

    def __init__(self, fName):
        self.path = '{dirPath}/CustomFunctions/f_{name}.py'.format(dirPath=os.getcwd(), name=fName)

    def addNewFunction(self, data):
        fileWriter = FileWriter()

        template = fileWriter.readFile('{dirPath}/CustomFunctions/{name}'.format(dirPath=os.getcwd(), name='customFunctionTemplate.txt'))
        fileWriter.writeToFile(self.path, template)
        fileWriter.addToFile(self.path, "\n\n" + data)