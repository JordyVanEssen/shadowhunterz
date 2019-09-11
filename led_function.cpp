#include <ThreadController.h>
#include <Thread.h>				
#include <StaticThreadController.h>

#include <FastLED.h>

// How many leds in your strip?
#define NUM_LEDS 290

// For led chips like Neopixels, which have a data line, ground, and power, you just
// need to define DATA_PIN.  For led chipsets that are SPI based (four wires - data, clock,
// ground, and power), like the LPD8806 define both DATA_PIN and CLOCK_PIN
#define DATA_PIN 3
#define CLOCK_PIN 13

// Define the array of leds
CRGB leds[NUM_LEDS];

Thread rainThread = Thread();

// the LED matrix
// --------|
// |-------|
// |-------
int led[17][17];

int x_max = 17;
int y_max = 17;
int counter = 0;
int lim = y_max - 1;

void setup() { 
  rainThread.enabled = true;
	rainThread.setInterval(200);

  Serial.begin(9600);
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
  mapLED();
}

void loop() { 
  for(int x = 0; x < x_max; x++){
    rainThread.onRun(rain(random(3, 8), x));

    if (rainThread.shouldRun())
    {
      rainThread.run();
      
      rainThread = Thread();
      rainThread.enabled = true;
	    rainThread.setInterval(200);
    }
      
  }
}


void rain(int dropLength, int pX){
  for(int y = 0; y < y_max; y++){
    FastLED.clear();
    leds[led[y][pX]] = CRGB(200,0,255);
    for(int drop = 0; drop < dropLength - 1; drop++){
      leds[led[y - drop][pX]] = CRGB(200, 0, 255);
    }
    FastLED.show();
    delay(random(30, 100));
  }
}


void mapLED(){
  for (int x = 0; x < x_max; x++)
  {
    lim = y_max - 1;
    if((x % 2 != 0)){
      for (int y = 0; y < y_max; y++)
      { 
        led[x][y] = (x * y_max) + (lim);
        lim--;
      }
    }
    else{
      lim = 0;
      for (int y = 0; y < y_max; y++)
      { 
        if(x == 0){
          led[x][y] = counter;
          counter++;
        }
        else{
          led[x][y] = led[x - 1][y] + (lim + (y + 1));
          lim++;
        }
      }
    }
  }

  for (int i = 0; i < x_max; i++){
    Serial.println( "\n: "+ i);
    for(int y =0; y < y_max; y++)
            Serial.println(led[i][y]) ;
  }
}



void drawSquare(int pos_x, int pos_y, int width, int R, int G, int B){
  for(int y = 0; y < width; y++)
  {
      for(int x = 0; x < width; x++)
      {

        
        leds[led[y+pos_y][x+pos_x]] = CRGB(R,G,B);
         
      }
  }
  FastLED.show();
}


void DrawMan(int moveX){
  FastLED.clear();
  
  // body
  drawSquare(8 + moveX, 10, 2, 0,0,255);
  drawSquare(8 + moveX, 8, 2, 0,0,255);
  drawSquare(8 + moveX, 7, 2, 0,0,255);

  // head
  drawSquare(7 + moveX, 3, 4, 255,0,0);

    // left leg
    leds[led[7][7 + moveX]] = CRGB(0,255,0);
    leds[led[7][6 + moveX]] = CRGB(0,255,0);
    leds[led[6][5 + moveX]] = CRGB(0,255,0);

    // right leg
    leds[led[7][10 + moveX]] = CRGB(0,255,0);
    leds[led[7][11 + moveX]] = CRGB(0,255,0);
    leds[led[6][12 + moveX]] = CRGB(0,255,0);

    // left arm
    leds[led[14][7 + moveX]] = CRGB(0,255,0);
    leds[led[13][7 + moveX]] = CRGB(0,255,0);
    leds[led[12][7 + moveX]] = CRGB(0,255,0);

    // right arm
    leds[led[14][10 + moveX]] = CRGB(0,255,0);
    leds[led[13][10 + moveX]] = CRGB(0,255,0);
    leds[led[12][10 + moveX]] = CRGB(0,255,0);
    
    
    FastLED.show();
}

/*turnOff(int pos_x, int pos_y){



  leds[led[pos_y][pos_x]] = CRGB(0,0,0);

  
  
}*/