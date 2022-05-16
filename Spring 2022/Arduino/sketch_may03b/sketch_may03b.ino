/* 
a dummy file to test AccelStepper.h
do not use and pls ignore 
 */
#include <AccelStepper.h>
#include <Arduino.h>

AccelStepper mystepper(2, 2, 3);

int counter = 0; 

void setup() {
  // put your setup code here, to run once:
  mystepper.setMaxSpeed(200.0);
  mystepper.setAcceleration(100.0);
  mystepper.setSpeed(200.0); 

}

void loop() {
//  i = i + 100; 
//    mystepper.runSpeed();
counter++; 
if (counter%4000 == 0) {
  counter = 10; 
  delay(200); 
}
    mystepper.move(500.0);
    mystepper.run();
}
