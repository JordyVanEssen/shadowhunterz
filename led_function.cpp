#include <stdio.h>
// the y and x axis 
int led[17][17];

int main(void) {
  //mapLED();
  generateCube(5, 2, 2);
}

void mapLED(){
  

  int x_max = 17;
  int y_max = 17;
  int counter = 0;
  int max = y_max - 1;

  for (int x = 0; x < x_max; x++)
  {
    max = y_max - 1;
    if((x % 2 != 0)){
      for (int y = 0; y < y_max; y++)
      { 
        led[x][y] = (x * 17) + (max);
        max--;
      }
    }
    else{
      max = 0;
      for (int y = 0; y < y_max; y++)
      { 
        if(x == 0){
          led[x][y] = counter;
          counter++;
        }
        else{
          led[x][y] = led[x - 1][y] + (max + (y + 1));
          max++;
        }
      }
    }
  }

  for (int i = 0; i < x_max; i++){
    printf( "\n%d: ", i);
    for(int y =0; y < y_max; y++)
            printf( "%d ", led[i][y]) ;
  }
}

// the x and y paramters are used as a starting point to draw the cube
void generateCube(int pSize, int pX, int pY){

  for(int y = 0; y < pSize; y++)
  {
      for(int x = 0; x < pSize; x++)
      {
        led[y + pY][x + pX] = CRGB::Red; 
      }
  }
}



