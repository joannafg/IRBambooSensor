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
  stepper1.setSpeed(30);
  stepper2.setSpeed(30);

  //Method 3
  sensor.setModel(SharpDistSensor::GP2Y0A51SK0F_5V_DS);
}

void loop() {
  int numSample = 100;
  double meanRaw = 0.0;
  int sum = 0;
  double methodOne = 0.0;
  double methodTwo = 0.0;
  double methodThree = 0.0;
  double methodFour = 0.0; 

//  if (digitalRead(PushSwitch) == HIGH) { //push the button to start the process
  if (Serial.available()) {
    //move the sensor to the bottom
//    while (limitSwitch.getState() == LOW) {
//      stepper2.step(1);
//    }
//      
//    delay(2000);

    //start 
    for (int j = 0; j < HEIGHT / HEIGHT_STEP; j++) {
      //turn table for loop
      for (int i = 0; i < 25; i++) {
        stepper1.step(32);
        delay(50);
        sum = 0;
        for (int k = 0; k < numSample; k++) {
          sum = sum + analogRead(IRPin);
          delay(0.1);
        }
        meanRaw = (sum / numSample);

        //        method 1
        //        https://electropeak.com/learn/interfacing-gp2y0a51sk0f-infrared-distance-sensor-with-arduino/
        methodOne = 4600.5 * pow(map(meanRaw, 0, 1023, 0, 5000), -0.94);

        //        method 2
        //        https://robojax.com/using-sharp-ir-gp2y0a51sk0f-distance-sensor-arduino-2cm-15cm
        float voltage_temp_average = 0;
        float MCU_Voltage = 5.0;
        for (int i = 0; i < numSample; i++)
        {
          int sensorValue = analogRead(IRPin);
          delay(0.1);
          voltage_temp_average += sensorValue * (MCU_Voltage / 1023.0);

        }
        voltage_temp_average /= numSample;
        methodTwo = 33.9 + -69.5 * (voltage_temp_average) + 62.3 * pow(voltage_temp_average, 2) + -25.4 * pow(voltage_temp_average, 3) + 3.83 * pow(voltage_temp_average, 4);

        //        method 3
        //        https://github.com/DrGFreeman/SharpDistSensor
        unsigned int methodThree = sensor.getDist();

        //        method 4 
        //        https://github.com/SuperMakeSomething/diy-3d-scanner/blob/master/scannerCode.ino
        methodFour=map(meanRaw,0.0,1023.0,0.0,5.0);
        methodFour =-5.40274*pow(methodFour,3)+28.4823*pow(methodFour,2)-49.7115*methodFour+31.3444;

        Serial.println("meanRaw: " + String(meanRaw, 4));
        Serial.println("methodOne: " + String(methodOne, 4));
        Serial.println("methodTwo: " + String(methodTwo, 4));
        Serial.println("methodThree: " + String(methodThree, 4));
        Serial.println("methodFour: " + String(methodFour, 4));
      }
      stepper2.step(-1000 * HEIGHT_STEP);
      delay(20);
    }
//    stepper2.step(HEIGHT * 1000);
  }
//  delay(100000);
}
