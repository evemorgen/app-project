import json
import sys
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timezone
from itertools import groupby

# python plotMetrics.py "metric-dump-1546730623.6767921.txt" "[10-177-54-70.files.assigned, 10-177-54-70.sockets.tcp_mem]"

def toDate(unix_timestamp):
    utc_time = datetime.fromtimestamp(unix_timestamp, timezone.utc)
    return utc_time.astimezone().strftime("%Y-%m-%d %H:%M:%S")

def plot(label, metricData):
    x = np.array(list(map(toDate, [x[1] for x in metricData])), dtype=np.datetime64)
    y = [x[0] for x in metricData]
    plt.style.use('seaborn-whitegrid')
    plt.plot(x, y, label = label)

path = sys.argv[1]
inputMetrics = sys.argv[2]

with open(path) as f:
    data = json.load(f)
    for metric, group in groupby(data, lambda x: x[0]):
        metricLabel = metric.split(".vm-")[1]
        if metricLabel in inputMetrics:
            for metricData in group:
                plot(metricLabel, metricData[1])
    plt.xlabel('Time')
    plt.ylabel('Something')
    plt.legend()
    plt.show()
