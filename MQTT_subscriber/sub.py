import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connect with result code" + str(rc))

    client.subscribe("channels/Light")

def on_message(client, userdata, msg):
    print(msg.topic+""+msg.payload.decode('utf-8'))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.0.7", 1883, 60)
client.loop_forever()
