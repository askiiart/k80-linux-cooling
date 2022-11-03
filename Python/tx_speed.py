import time
from subprocess import getoutput
try:
    import GPUtil
    from pySerialTransfer import pySerialTransfer as txfer
    from serial import SerialException
except ImportError:
    print('Make sure you have installed the required libraries: GPUtil, pySerialTransfer')

try:
    # ---
    # You will need to customize port to your own computer; to find your port:
    # With your Arduino plugged in, open Arduino IDE, and click "Select Board". Then, you can see the port.
    # The port of the Uno will be "/dev/ttyXXX#", like "/dev/ttyACM0" or "/dev/ttyUSB0". I think macOS is the same.
    # Then, just remove "/dev/", and the number, from the port, and type it into the variable `port`
    # ---
    
    def get_port():
        port = 'ttyACM'
        while True:
            ports = getoutput(f'ls /dev | grep {port}').split('\n')
            if ports != ['']:
                ports.sort()
                port = ports[len(ports) - 1]
                break
            print('Waiting for Arduino...')
            time.sleep(3)
    
        return port
    
    link = txfer.SerialTransfer(get_port(), 115200, timeout=.1)
    link.open()

    while True:
        
        try:
            time.sleep(1)
            gpus = GPUtil.getGPUs()
            temp = max(gpu.temperature for gpu in gpus)

            speed = int(((temp - 40) / 40) * 100)
            min_speed = 34
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
        except OSError or SerialException:
            try:
                link.close()
            except:
                pass
            link = txfer.SerialTransfer(get_port(), 115200, timeout=.1)
            link.open()


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
