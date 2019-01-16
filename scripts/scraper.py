import hashlib
import json
import logging
from tornado.httpclient import HTTPClient
from time import sleep, time


def make_request(purchase_key, metric, time, api_key):
    url = f'{purchase_key}.maasprovider.dreamlab.pl/api/render?from=-{time}&until=now&target={metric}&format=json'
    val = url + api_key
    sign = hashlib.md5()
    sign.update(val.encode('utf-8'))
    headers = {'Authorization': 'MaaS ' + sign.hexdigest()}
    client = HTTPClient()
    res = client.fetch('http://' + url, headers=headers)
    return json.loads(res.body.decode('utf-8'))


results = []
logging.basicConfig(level=logging.INFO, filename='/vol0/dumps/worklog.log', filemode='w')
api_key = sys.argv[1]
purchase_key = sys.argv[2]
data = json.loads(open('maas_leafs.txt', 'r').read())
i = 0
for metric in data:
    try:
        res = make_request(purchase_key, metric, '7days', api_key)
        results.append(res)
        i += 1
        logging.info(f"[{i}/{len(data)}] - {metric}")
        if i % 100 == 0:
            logging.info("saving results")
            open(f'/vol0/dumps/metric-dump-{time()}.txt', 'a').write(json.dumps(results))
            results = []
    except Exception:
        logging.error(f"Oppsie - {metric}")
    sleep(0.33)
