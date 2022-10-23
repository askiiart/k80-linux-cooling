import GPUtil
import time

from pySerialTransfer import pySerialTransfer as txfer

try:
    # ---
    # You will need to customize port to your own computer; to find your port:
    # With your Arduino plugged in, open Arduino IDE, and click "Select Board". Then, you can see the port.
    # On Linux, it will be "/dev/ttyXXX#", like "/dev/ttyACM0" or "/dev/ttyUSB0". I think macOS is the same.
    # On Windows, it will be "COM#", like "COM3"
    # ---
    port = '/dev/ttyACM0'
    link = txfer.SerialTransfer(port, 115200, timeout=.1)

    link.open()
    time.sleep(2)

    # GPUtil setup
    gpus = GPUtil.getGPUs()

    while True:
        time.sleep(1)
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
        while not link.available():
            if link.status < 0:
                if link.status == txfer.CRC_ERROR:
                    print('Error: CRC_ERROR')
                elif link.status == txfer.PAYLOAD_ERROR:
                    print('Error: PAYLOAD_ERROR')
                elif link.status == txfer.STOP_BYTE_ERROR:
                    print('Error: STOP_BYTE_ERROR')
                else:
                    print('Error: {}'.format(link.status))

        # Parse response from Arduino
        rec_int = link.rx_obj(obj_type=int, obj_byte_size=int_size, start_pos=(send_size - int_size))

        # Evaluate for comm. errors
        if speed != rec_int:
            print(f'Error: sent {speed}, received {rec_int}')

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
