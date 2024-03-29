# Universal K80 Cooling

This is a Linux cooling control software, which uses an Arduino Uno, PWM fan, and Python 3. It was designed for use with a Tesla K80 (a datacenter GPU without fans), but should work with any NVIDIA GPU.

This will determine the speed your fan (connected to your Arduino) should run at based on the highest temperature 
between your GPUs, then will send that speed to your Arduino. 

Make sure to set the port in the .py file you use!

### How to use
1. Install dependencies using `pip install -r requirements.txt`
2. Connect the Arduino to the fan according to this diagram. Keep in mind that if you're powering the fan through the arduino, as is the case here, the fan can only be up to 1 amp.
![PWM connected to pin 9, TACH not connected](Images/arduino-fan-diagram.png)
3. **Set the port variable** 
   1. Instructions for finding the port are in the Python code.
4. Create a script to run this every 10 seconds
   1. Use a text editor to create a script called `every5secs.sh, and add the code below.
   2. Make a note of where you saved the script, and remember to change `/path/to/tx_cron.py`
```bash
# This runs the tx_cron.py every 10 seconds
i=0

while [ $i -lt 6 ]; do # 6 ten-second intervals in 1 minute
  python3 /path/to/tx_cron.py & #run your command
  sleep 10
  i=$(( i + 1 ))
done
```
4. Create a cron job
   1. Run `crontab -e`
   2. Add this line to the bottom of the file: `* * * * * python3 /path/to/every5secs.sh`
      1. Remember to change the path to your script!
   3. Save and exit with `Escape`, `:wq`, `Enter`

### My setup
- I use [this](https://www.thingiverse.com/thing:4960323) 3D-printed fan adapter for my Tesla K80; I highly recommend it.
  - I also remixed it into a 92mm version [here](https://www.thingiverse.com/thing:5408988)!
- Also, I use [this](https://www.amazon.com/Wathai-Airflow-Speed-Pressure-Cooling/dp/B07Z4JZPKN) fan. It's pretty powerful, and pretty loud!
  - Note: I couldn't get PWM to work properly with this fan. Maybe get a Delta one if you want that.

### Notes and Limitations:
 - This currently **only supports NVIDIA GPUs**
 - This currently **only supports normal PWM**, not delta PWM
 - You *may* need to change some variables in the Arduino code depending on your fan's specifications.
   - Try looking up a datasheet
 - This was designed for an Arduino Uno, and should work on one. I don't know about running it on anything else, though.
 - `tx_speed.py` works fine, but it's just an infinite loop. I'm working on marking a version that uses a cron job, but it's not done yet.

### Resources I used
- Python-Arduino communications library - [pySerialTransfer](https://github.com/PowerBroker2/pySerialTransfer)
  - Thanks for the help figuring this out, [PowerBroker2](https://github.com/PowerBroker2)!
- Arduino PWM fan control - [25 kHz 4 Pin PWM Fan Control with Arduino Uno](https://create.arduino.cc/projecthub/tylerpeppy/25-khz-4-pin-pwm-fan-control-with-arduino-uno-3005a1)
  - This is the basis of my arduino-fan diagram
- See NVIDIA GPU temperatures - [GPUtil](https://pypi.org/project/GPUtil/)

### TODO
- Add diagram for wiring LED lights
