import Adafruit_DHT
import time
sensor = Adafruit_DHT.DHT11
pin = 4
hum, temp = Adafruit_DHT.read_retry(sensor, pin)

while hum is not None and temp is not None:
    print("Temp={0:0.1f}* Hum={1:0.1f}%".format(temp, hum))
    print(temp)
    print(hum)
    time.sleep(20)
else:
    print("Failed")
    sys.exit(1)
