# How to deploy
Here are some yaml file for deploy my system.
For our system, we have one PC as our cloud node; one Raspberry pi 4 as our edge node.
In both cloud node and edge node have a influxdb deployment and a grafana deployment. The example yaml file you can get under this folder.

## Get start
After you initialize your kubeedge cluster (in my system I use Kubeedge v1.4 version), We deploy Influxdb first.

> Notice that I use nodeSelector to select which node I want to deploy, in my case I tag my node as following:
```=cmd
# label cloud node
kubectl label node k8s-node01 name=k8s-node01

# label edge node
kubectl label node raspberrypi name=edge-1
```
If you want to change label, remenber to rewrite the YAML file before deploy it. You can find "nodeSelector" field on the button of YAML.

* Create directory
At edge node and cloud node.
```=cmd
sudo mkdir /mnt/influxdb
sudo mkdir /mnt/grafana
sudo chmod 777 /mnt/influxdb
sudo chmod 777 /mnt/grafana
```

### InfluxDB
* Create secret
```=cmd
kubectl create secret generic influxdb-creds \
  --from-literal=INFLUXDB_DATABASE=db \
  --from-literal=INFLUXDB_USERNAME=telegraf \
  --from-literal=INFLUXDB_PASSWORD=telegraf \
  --from-literal=INFLUXDB_HOST=influxdb
```

* deploy influxdb at edge node.
```=cmd
kubectl apply -f edge-influxdb.yaml
```

* deploy influxdb at cloud node.
```=cmd
kubectl apply -f cloud-influxdb.yaml
```

### Grafana
* deploy grafana at edge node.
```=cmd
kubectl apply -f edge-grafana.yaml
```

* deploy grafana at cloud node.
```=cmd
kubectl apply -f cloud-grafana.yaml
```
### Subscribe to ESP8266

