import Adafruit_DHT
import time

import json
from influxdb import InfluxDBClient
from datetime import datetime, timezone, timedelta

# dht11 setup
sensor = Adafruit_DHT.DHT11
pin = 4
hum, temp = Adafruit_DHT.read_retry(sensor, pin)

# influxdb connect
dbClient = InfluxDBClient('192.168.0.7', '8086', 'telegraf', 'telegraf', 'db0')

while hum is not None and temp is not None:
    # get current time
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=0))) # timezone: UTC+8
    data_time = dt2.strftime("%Y-%m-%d %H:%M:%S")

    # show data
    print("Temp={0:0.1f}* Hum={1:0.1f}%".format(temp, hum))

    # data wrap in json, send to influxDB
    toDB_json = [{
        "measurement": "dht11",
        "time": data_time,
        "tags":{
            'device': "Raspberry pi 4"
            },
        "fields":{
            'Temp': temp,
            'Hum': hum
            }
        }]
    dbClient.write_points(toDB_json)
    time.sleep(20)
else:
    print("Get DHT11 data failed!")
    sys.exit(1)
