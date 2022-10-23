# Universal K80 Cooling

This will determine the speed your fan (connected to your Arduino) should run at based on the highest temperature 
between your GPUs, then will send that speed to your Arduino. 

---

### How to use
1. Connect the Arduino to the fan according to this diagram:
![https://create.arduino.cc/projecthub/tylerpeppy/25-khz-4-pin-pwm-fan-control-with-arduino-uno-3005a1](Images/arduino-fan-diagram.png)
   1. #### Connect to the PWM wire, not TACH as is shown there! The color may change depending on your model of fan!
      1. Sorry for not making another diagram, I couldn't find any decent way to do so. Once I make a new diagram, I'll 
2. Connect the Arduino to your PC via USB, then find the port it's on and **set the port variable**. 
   1. Instructions for finding the port are in the Python code.
3. Revel in your success!
   1. If you plan to use this constantly, make sure to create a service that starts the Python code on boot.

### My setup
I use [this](https://www.thingiverse.com/thing:4960323) 3D-printed fan adapter for my Tesla K80; I highly recommend it.

In the long-term, I'm planning to build my own front cover for my PC case (a Corsair 175R), and will have a spot for my 
Arduino and wiring in it.

Pictures will be added later once my setup is complete. Don't expect it to happen anytime soon, though.

---

### Notes and Limitations:
 - This currently **only supports NVIDIA GPUs**
 - This currently **only supports normal PWM**, not delta PWM
 - **You will need to set the port of your arduino manually** (in the Python code as the `port` variable)
   - There are instructions on how to find the port in the code
 - Your **fan may use a different color scheme** for its wire, or have a black color scheme. Be sure to 
Google a diagram first.
 - You may need to change some variables in the Arduino code depending on your fan's specifications.
   - Try looking up a datasheet
 - This was designed for an Arduino Uno, and should work on one. I don't know about running it on anything else, though.

---

### Resources I used
- Python-Arduino communications library - [pySerialTransfer](https://github.com/PowerBroker2/pySerialTransfer)
- Arduino PWM fan control - [25 kHz 4 Pin PWM Fan Control with Arduino Uno](https://create.arduino.cc/projecthub/tylerpeppy/25-khz-4-pin-pwm-fan-control-with-arduino-uno-3005a1)
  - This is where I got the arduino-fan diagram from.