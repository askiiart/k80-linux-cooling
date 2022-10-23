int pin1 = 8;
int pin2 = 7;
int pin3 = 6;
int pin4 = 5;
int pin5 = 4;
int pin6 = 3;
int pin7 = 2;

void setup() {
}

void loop() {
  // put your main code here, to run repeatedly:
  int x = 101;
  if((x % 2) > 0) { digitalWrite(pin1, HIGH); } else { digitalWrite(pin1, LOW); }
  if((x % 4) > 1) { digitalWrite(pin2, HIGH); } else { digitalWrite(pin2, LOW); }
  if((x % 8) > 3) { digitalWrite(pin3, HIGH); } else { digitalWrite(pin3, LOW); }
  if((x % 16) > 7) { digitalWrite(pin4, HIGH); } else { digitalWrite(pin4, LOW); }
  if((x % 32) > 15) { digitalWrite(pin5, HIGH); } else { digitalWrite(pin5, LOW); }
  if((x % 64) > 31) { digitalWrite(pin6, HIGH); } else { digitalWrite(pin6, LOW); }
  if((x % 128) > 63) { digitalWrite(pin7, HIGH); } else { digitalWrite(pin7, LOW); }
}
