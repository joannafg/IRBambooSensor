#include <Stepper.h>
#include <Arduino.h>
#include <SharpDistSensor.h>
#include <ezButton.h>

#define STEPS 200
#define IRPin A0
#define PushSwitch 8 
#define motorInterfaceType 1
#define HEIGHT 30//in cm
#define HEIGHT_STEP 1//in cm 

// Create variable to store the distance:
int distance_cm;

// Define stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver
Stepper stepper1(STEPS, 2, 3); //turn table
Stepper stepper2(STEPS, 4, 5); //sensor

ezButton limitSwitch(7);  // create ezButton object that attach to pin 7;


//Method 3
// Analog pin to which the sensor is connected
const byte sensorPin = A0;
// Window size of the median filter (odd number, 1 = no filtering)
const byte medianFilterWindowSize = 1;
// Create an object instance of the SharpDistSensor class
SharpDistSensor sensor(sensorPin, medianFilterWindowSize);

void setup() {
  Serial.begin(9600);
  Serial.flush();
  // Set the maximum speed in steps per second:
  stepper1.setSpeed(30); // Decrease the speed to 10 if it has any problem
  stepper2.setSpeed(30);

  //Method 3
  sensor.setModel(SharpDistSensor::GP2Y0A51SK0F_5V_DS);
}

void loop() {
  int numSample = 3;
  double meanRaw = 0.0;
  int sum = 0;
  double methodOne = 0.0;
  double methodTwo = 0.0;
  double methodThree = 0.0;
  double methodFour = 0.0; 

  if (Serial.available()) {

    //start 
    for (int h = 0; h < HEIGHT * 1000; h++) {
      stepper1.step(1);
      stepper2.step(-1);
      meanRaw = analogRead(IRPin);
      methodOne = 4600.5 * pow(map(meanRaw, 0, 1023, 0, 5000), -0.94);
      Serial.println("meanRaw: " + String(meanRaw, 4));
      Serial.println("methodOne: " + String(methodOne, 4));
      //delayMicroseconds(50);    add this line if it does not turn properly. test number from 20 to 100
    }
    
    
    delay(100000);
  }
}
