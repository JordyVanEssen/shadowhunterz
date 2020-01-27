from os.path import dirname, basename, isfile, join
import os
import glob

class control:
    def __init__(self):
        pass
    
    # return all the custom functions
    def getAll(self):
        modules = glob.glob(join(dirname(__file__), "*.py"))
        self.__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py') and not f.endswith('cControl.py')]
        print(self.__all__)
        return self.__all__

    # checks if a given exists
    def ifMethodExist(self, name):
        modules = glob.glob(join(dirname(__file__), "*.py"))
        self.__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py') and not f.endswith('cControl.py')]
        if "f_" + name in self.__all__:
            return True
        else:
            return False
