FROM python:3.7.9-slim-stretch

COPY requirements.txt /cmd/requirements.txt
COPY sub_v2.py /cmd/sub_v2.py
COPY backup.py /cmd/backup.py

RUN pip3 install -r /cmd/requirements.txt
