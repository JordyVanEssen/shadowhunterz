from cCoordinate import Coordinate

class Calculations:
    X_MAX = 0
    Y_MAX = 0

    SQUARE_X = 0
    SQUARE_Y = 0

    def __init__(self, xmax, ymax, sqaure_x, square_y):
        self.X_MAX = xmax
        self.Y_MAX = ymax
        self.SQUARE_X = sqaure_x
        self.SQUARE_Y = square_y
        self.__self__ = self

    def calculateLeds(self, x, y):
        y += 1
        if y % 2 != 0:
            return (x + ((y - 1) * self.X_MAX))
        else:
            return ((((y - 1) * self.X_MAX)) + (self.X_MAX - x)) - 1

    def sensorCoordToLedCoord(self, x, y):
        return (y * self.Y_MAX + x)


    def calculateSensorCoord(self, sensorId):
        sensorId -= 1
        rest = sensorId
        yresult = 0

        for i in range(self.SQUARE_Y):
            if rest >= self.SQUARE_X:
                rest -= self.SQUARE_Y
                yresult += 1
        
        return Coordinate(rest + 1, yresult + 1)

    def calcLEDS(self, num, x):
        x1 = num
        x2 = num + 1
        x3 = num + (((2 * self.X_MAX)-1) - ((x-1) * 4))-1
        x4 = x3 + 1
        arr = {x1, x2, x3, x4}
        print(arr)
        return arr

    def calcTopLeftSquare(self, x, y):
        return x * 2 - 1 + (((y*2-1)-1) * self.Y_MAX)