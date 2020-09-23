import paho.mqtt.client as mqtt
import random
import json  
import datetime 
import time

# 設置日期時間的格式
ISOTIMEFORMAT = '%m/%d %H:%M:%S'

# 連線設定
# 初始化地端程式
client = mqtt.Client()

# 設定登入帳號密碼

# 設定連線資訊(IP, Port, 連線時間)
client.connect("192.168.0.7", 1883, 60)

while True:
    heart = random.randint(66,90)
    t = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    payload = {'beatsPerMinute' : heart }
    print (json.dumps(payload))
    #要發布的主題和內容
    client.publish("channels/heartrate/", json.dumps(payload))
    time.sleep(1)
