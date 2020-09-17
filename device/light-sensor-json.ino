#include <ESP8266WiFi.h> 
#include <PubSubClient.h>
const char* ssid = "D-Link_DIR-612";
const char* password = "055260322";
const char* mqttServer = "192.168.0.7";  // MQTT伺服器位址
const char* clientID = "Light";      // 用戶端ID，隨意設定。
const char* topic = "channels/light/";

unsigned long prevMillis = 0;  // 暫存經過時間（毫秒）
const long interval = 2000;  // 上傳資料的間隔時間，2秒。
String msgStr = "";      // 暫存MQTT訊息字串

char json[25];

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
}

void reconnect() {
  while (!client.connected()) {
    //if (client.connect(clientID, mqttUserName, mqttPwd)) {
    if (client.connect(clientID)){
      Serial.println("MQTT connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 4 seconds");
      delay(4000);  // 等4秒之後再重試
    }
  }
}

void setup() {
  Serial.begin(9600);
  setup_wifi();
  client.setServer(mqttServer, 1883);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // 等待2秒
  if (millis() - prevMillis > interval) {
    prevMillis = millis();

    // 讀取DHT11的溫濕度資料
    int sensorValue = analogRead(A0);

    // 組合MQTT訊息；field1填入溫度、field2填入濕度
    //msgStr=msgStr+"Light="+sensorValue;
    msgStr = msgStr  + "{\"Light\":" + (sensorValue) + "}";
    
    // 宣告字元陣列
    //byte arrSize = msgStr.length() + 1;
    //char msg[arrSize];
    msgStr.toCharArray(json, 25);
    
    
    Serial.print("Publish message: ");
    Serial.println(msgStr);
    //msgStr.toCharArray(msg, arrSize); // 把String字串轉換成字元陣列格式
    
    client.publish(topic, json);
    //client.publish(topic, msg);       // 發布MQTT主題與訊息
    msgStr = "";
  }
}
