#include <stdio.h>

int main(void) {
  int led[17][17];
  int x_max = 17;
  int y_max = 17;
  int counter = 0;
  int num = 16;

  for (int x = 0; x < x_max; x++)
  {
    num = 16;
    if((x % 2 != 0)){
      for (int y = 0; y < y_max; y++)
      { 
        led[x][y] = (x * 17) + (num);
        num--;
      }
    }
    else{
      num = 0;
      for (int y = 0; y < y_max; y++)
      { 
        if(x == 0){
          led[x][y] = counter;
          counter++;
        }
        else{
          led[x][y] = led[x - 1][y] + (num + (y+1));
          num++;
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



