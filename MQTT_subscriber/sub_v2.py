import paho.mqtt.client as mqtt
import json
from influxdb import InfluxDBClient
from datetime import datetime, timezone, timedelta

# influxdb connect
dbClient = InfluxDBClient('192.168.0.7', '8086', 'telegraf', 'telegraf', 'db0')

def on_connect(client, userdata, flags, rc):
    print("Connect with result code" + str(rc))

    client.subscribe("channels/Light")

def on_message(client, userdata, msg):
    # log output subscribe data
    print(msg.topic+""+msg.payload.decode('utf-8'))

    # data extract
    extract_light = sensorData(msg.payload.decode('utf-8'))

    print(type(extract_light))
    
    # get current time
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # timezone: UTC+8
    time = dt2.strftime("%Y-%m-%d %H:%M:%S")

    # data wrap in json, send to influxDB
    toDB_json = [{
        "measurement": 'Sensor',
        "time": time,
        "tags":{
            'location': "Dormitory"
            },
        "fields":{
            'light': extract_light
            }
        }]
    dbClient.write_points(toDB_json)

def sensorData(data):
    data = json.loads(data)
    light = data["Light"]
    return light

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.0.7", 1883, 60)
client.loop_forever()
