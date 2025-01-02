#include <Wire.h>

const int ledPin1 = 9;
const int ledPin2 = 8;

void setup() {
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  //digitalWrite(ledPin1, 0);
  //digitalWrite(ledPin2, 0));
  Wire.begin(8); // Join I2C bus with address 8
  Wire.onReceive(receiveEvent); // Register event for receiving data
}

void loop() {
  // No need for loop() as LED states are controlled by I2C
  delay(100); // Optional: Add a small delay for stability
}

void receiveEvent(int bytes) {
  byte data = Wire.read(); // Read the byte sent by the master

  // Decode the data (example: first bit for LED1, second bit for LED2)
  digitalWrite(ledPin1, bitRead(data, 0));
  digitalWrite(ledPin2, bitRead(data, 1));
}