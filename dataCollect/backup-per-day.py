import sys
import traceback
import json
from influxdb import InfluxDBClient
from datetime import datetime, timezone, timedelta

# edge influxdb connect
edgedb = InfluxDBClient('192.168.0.7', '8086', 'telegraf', 'telegraf', 'db0')
clouddb = InfluxDBClient('192.168.0.3', '8086', 'telegraf', 'telegraf', 'LightSensorBackup')

# query data from edge db
result = edgedb.query('select * from Sensor where time > now() - 1')
result_list = list(result.get_points())

# upload to cloud
try:
    for i in range (len(result_list)):
        write_json = [{
            "measurement": "Sensor",
            "time": result_list[i]['time'],
            "tags":{
                'location': result_list[i]['location']
                },
            "fields":{
                'light': result_list[i]['light']
                }
            }]
        clouddb.write_points(write_json)
except Exception as e:
    error_class = e.__class__.name__
    detail = e.args[0]
    cl, exc, tb = sys.exc_info()
    lastCallStack = traceback.extract_tb(tb)[-1]
    fileName = lastCallStack[0]
    lineNum = lastCallStack[1]
    funcName = lastCallStack[2]
    errMsg = "File \"{}\", line{}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    print(errMsg)
else:
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
    # delete edgedb data which just backup
    start_time = result_list[0]['time']
    end_time = result_list[len(result_list) - 1]['time']
    delete_cmd = "delete from Sensor where time >= '" + start_time + "' and time <= '" + end_time +"'"
    edgedb.query(delete_cmd)
    print('Backup' + str(len(result_list)) + 'data')
    print('from' + result_list[0]['time'] + 'to' + result_list[len(result_list)]['time'])
    print('Backup finish ...')
    print('timestamp: '+ d2.strftime("%Y-%m-%d %H:%M:%S"))
