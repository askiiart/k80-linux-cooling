import GPUtil
import time

gpus = GPUtil.getGPUs()

while True:
    print(str(max(gpu.temperature for gpu in gpus)) + " C")
    time.sleep(3)
