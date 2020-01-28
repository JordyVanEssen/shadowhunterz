// Wire Slave Sender
// by Nicholas Zambetti <http://www.zambetti.com>

// Demonstrates use of the Wire library
// Sends data as an I2C/TWI slave device
// Refer to the "Wire Master Reader" example for use with this

// Created 29 March 2006

// This example code is in the public domain.

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// Which pin on the Arduino is connected to the NeoPixels?
#define PIN        6 // On Trinket or Gemma, suggest changing this to 1

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 12 // Popular NeoPixel ring size

// When setting up the NeoPixel library, we tell it how many pixels,
// and which pin to use to send signals. Note that for older NeoPixel
// strips you might need to change the third parameter -- see the
// strandtest example for more information on possible values.
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);



#include <Wire.h>


#define Rp A0
#define Gp A2
#define Bp A3

int rgb[3];

int c =0;

int R, G, B;
int Rprev, Gprev, Bprev;

void setup() {
  #if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif
  // END of Trinket-specific code.

  pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
  pixels.setBrightness(100);
  pixels.clear();


  pinMode(Rp, INPUT);
  pinMode(Gp, INPUT);
  pinMode(Bp, INPUT);

  Serial.begin(9600);
  Wire.begin(3);                // join i2c bus with address #8
  Wire.onRequest(requestEvent); // register event
}

void loop() {
  //uitlezen


//Serial.println(analogRead(Rp));
  rgb[0] = map(analogRead(Rp), 0, 1023, 0, 255);
  rgb[1] = map(analogRead(Gp), 0, 1023, 0, 255);
  rgb[2] = map(analogRead(Bp), 0, 1023, 0, 255);

  R = rgb[0];
 G = rgb[1];
  B = rgb[2];

//rgb[2]= 0;
//rgb[1]= 0;
//
//rgb[0]=255;

    for(int a =0 ; a<3;a++){
  
  
        Serial.print(rgb[a]);
       Serial.print(",");
  
    }
    Serial.println("");
    for(int i=0; i<NUMPIXELS; i++) { // For each pixel...

    // pixels.Color() takes RGB values, from 0,0,0 up to 255,255,255
    // Here we're using a moderately bright green color:
    pixels.setPixelColor(i, pixels.Color(rgb[0], rgb[1], rgb[2]));

       // Send the updated pixel colors to the hardware.

    delay(10); // Pause before next pass through loop
  }

pixels.show();
  }




  // function that executes whenever data is requested by master
  // this function is registered as an event, see setup()
  void requestEvent(){
      //RGB waardes worden alleen verstuurd als ze verschillen van de vorige keer dat ze zijn verstuurd 
   
      Wire.write(rgb[c]);

     c++;
     
     if(c==3){

      c=0;
     }

    
  }
