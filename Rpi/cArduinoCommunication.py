
import smbus

class I2Csetup():
    ARDUINO_ADDRESS = None
    # Create the I2C bus 
    bus = smbus.SMBus(1) 
    on = False

    def __init__(self, arduinoAdress):
        self.ARDUINO_ADDRESS = arduinoAdress


    # This function converts a string to an array of bytes. 
    def ConvertStringToBytes(self, src):
        try:
            self.bus.write_byte_data(ARDUINO_ADDRESS, 0x00, ord(src))
            #print("Sent: %d" %ord(src))
        except:
            print("Error occured in the sending")


    # gets the input of the arduinos
    def readInput(self, address):
        data = self.bus.read_byte(int(address))
        if data > 0:
            print("received: %d" %data)
        
        if not (data is None):
            return data 
        else:
            return -1