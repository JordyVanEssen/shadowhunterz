//Arduino code to receive I2C communication from Raspberry Pi
 
#include <Wire.h>

// ============================================================================================================================
// These are the default settings for a slave used on a panel.
// Change these variables according to your layout.

// There are 3 slaves on 1 panel, each of them need an unique id. (0, 1 or 2)
const int slaveId = 2;
// The panel it is mounted on. Starting with 0.
const int panelId = 1;
// The amount of sensors used on this 1 panel
const int totalSensors = 144;
// The pins 0 and 1 are  not used 
const int connectedSensors = 48;

// Define the slave address of this device.
// The adresses start from 0x04
// When defining the address, 
// there cant be any duplicates of addresses so keep counting when you give the slaves of the next panel their address.
#define SLAVE_ADDRESS 0x09

// =========================================================================================================================== 

int sensorState = 1;
int previous = -1;
int squares[connectedSensors];


void setup() {
  // begin running as an I2C slave on the specified address
  //Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  
  int pin = 2;
  for(int i = 0; i < connectedSensors; i++){
    squares[i] = pin;
    
    if(pin == 19){
      pin += 3;
    }
    else{
      pin++;
    }
  }

  for(int i = 0; i < connectedSensors; i++){
    pinMode(squares[i], INPUT);
  }
     
  Wire.onRequest(onRequest);
}
 
void loop() {
  // keep looping over the array of pins, it is faster then looping when the pi asks for it.
  sensorState = readSensor();
  
}

void onRequest(){
    if(previous != sensorState){
        previous = sensorState;
        Wire.write(sensorState + 1);
    }
}
 
int readSensor(){
    for (int i = 0; i < connectedSensors; i++)
    {
        // loop over all the pins  
        int state = digitalRead(squares[i]);
        //Serial.print(i);
        //Serial.print(" ");
        //Serial.println(state);
        // if activated, send the index of the array + the id * connectedSensors
        // keep in mind for the last slave this wont work, because it does not have as many sensors connected to it.
        // so you need to change connectedSensors to the amount of sensors connected to both of the other slaves + all the senors on previous panels.
        if (state == 0)
            return (i + (slaveId * connectedSensors)) + (panelId * totalSensors);        
    }
    return -1;
}
