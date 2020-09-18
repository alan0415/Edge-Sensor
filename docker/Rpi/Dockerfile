FROM arm32v7/python:3.7.9

COPY requirements.txt /cmd/requirements.txt
COPY esp8266.py /cmd/esp8266.py
COPY backup.py /cmd/backup.py
COPY dht11.py /cmd/dht11.py

RUN pip3 install -r /cmd/requirements.txt
