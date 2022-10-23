#include "SerialTransfer.h"

// This program will take an number from the PC and display it using LEDs to represent it as a binary number

SerialTransfer myTransfer;

const byte OC1A_PIN = 9;
const byte OC1B_PIN = 10;

const word PWM_FREQ_HZ = 25000; //Adjust this value to adjust the frequency (Frequency in HZ!) (Set currently to 25kHZ)
const word TCNT1_TOP = 16000000/(2*PWM_FREQ_HZ);

int pin1=8;  //initializing pins as vars because who wants to use constants:
int pin2=7;
int pin3=6;
int pin4=5;
int pin5=4;
int pin6=3;
int pin7=2;

void setup() {
  // Setup Serial transfer with PC
  Serial.begin(115200);
  myTransfer.begin(Serial);

  pinMode(OC1A_PIN, OUTPUT);

  // Clear Timer1 control and count registers
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1  = 0;

  // Set Timer1 configuration
  // COM1A(1:0) = 0b10   (Output A clear rising/set falling)
  // COM1B(1:0) = 0b00   (Output B normal operation)
  // WGM(13:10) = 0b1010 (Phase correct PWM)
  // ICNC1      = 0b0    (Input capture noise canceler disabled)
  // ICES1      = 0b0    (Input capture edge select disabled)
  // CS(12:10)  = 0b001  (Input clock select = clock/1)

  TCCR1A |= (1 << COM1A1) | (1 << WGM11);
  TCCR1B |= (1 << WGM13) | (1 << CS10);
  ICR1 = TCNT1_TOP;
}

void loop() {

  if(myTransfer.available())
  {

    // send all received data back to Python
    for(uint16_t i=0; i < myTransfer.bytesRead; i++){
      myTransfer.packet.txBuff[i] = myTransfer.packet.rxBuff[i];
    }
    myTransfer.sendData(myTransfer.bytesRead);

	int x = int(myTransfer.packet.rxBuff);
    if((x % 2) > 0) { digitalWrite(pin1, HIGH); } else { digitalWrite(pin1, LOW); }
    if((x % 4) > 1) { digitalWrite(pin2, HIGH); } else { digitalWrite(pin2, LOW); }
    if((x % 8) > 3) { digitalWrite(pin3, HIGH); } else { digitalWrite(pin3, LOW); }
    if((x % 16) > 7) { digitalWrite(pin4, HIGH); } else { digitalWrite(pin4, LOW); }
    if((x % 32) > 15) { digitalWrite(pin4, HIGH); } else { digitalWrite(pin4, LOW); }
    if((x % 64) > 31) { digitalWrite(pin4, HIGH); } else { digitalWrite(pin4, LOW); }
    if((x % 128) > 63) { digitalWrite(pin4, HIGH); } else { digitalWrite(pin4, LOW); }
  }
}

void setPwmDuty(byte duty) {
  OCR1A = (word) (duty*TCNT1_TOP)/100;
}
