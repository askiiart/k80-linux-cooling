import time
from subprocess import getoutput

import GPUtil
from pySerialTransfer import pySerialTransfer as txfer

try:
    # ---
    # You will need to customize port to your own computer; to find your port:
    # With your Arduino plugged in, open Arduino IDE, and click "Select Board". Then, you can see the port.
    # The port of the Uno will be "/dev/ttyXXX#", like "/dev/ttyACM0" or "/dev/ttyUSB0". I think macOS is the same.
    # Then, just remove "/dev/", and the number, from the port, and type it into the variable `port`
    # ---

    port = 'ttyACM'
    ports = getoutput(f'ls /dev | grep {port}').split('\n')
    if ports != ['']:
        ports.sort()
        port = ports[len(ports) - 1]

    link = txfer.SerialTransfer(port, 115200, timeout=.1)

    link.open()
    time.sleep(2)

    gpus = GPUtil.getGPUs()
    temp = max(gpu.temperature for gpu in gpus)

    speed = int(((temp - 40) / 40) * 100)
    min_speed = 0
    max_speed = 100
    if speed < 0:
        speed = min_speed
    elif speed > 100:
        speed = max_speed

    print(f'Temp: {temp}')
    print(f'Speed: {speed}')

    ################################################################################################################
    # Send data to the Arduino
    ################################################################################################################

    # send_size will be increased when data is added to payload
    send_size = 0

    # Adds data to payload
    int_size = link.tx_obj(speed, send_size) - send_size
    send_size += int_size

    # Sends data to Arduino
    link.send(send_size)

    # Waits for response from Arduino, and reports errors while receiving packets
    current_time = time.strftime("%H:%M:%S", time.localtime())
    error = current_time
    while not link.available():
        if link.status < 0:
            if link.status == txfer.CRC_ERROR:
                error += ': CRC_ERROR'
            elif link.status == txfer.PAYLOAD_ERROR:
                error += ': PAYLOAD_ERROR'
            elif link.status == txfer.STOP_BYTE_ERROR:
                error += ': STOP_BYTE_ERROR'
            else:
                print('Error: {}'.format(link.status))

    link.close()

except KeyboardInterrupt:
    try:
        link.close()

    except:
        pass

except:
    import traceback

    traceback.print_exc()

    try:
        link.close()

    except:
        pass
