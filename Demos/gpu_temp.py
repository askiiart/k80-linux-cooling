import GPUtil
import time

gpus = GPUtil.getGPUs()
gpu = gpus[0]

while True:
    print(str(gpu.temperature) + " C")
    time.sleep(3)
