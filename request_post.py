import json
import time

import requests
from trex_test.test_path import *
from trex.examples.stl.stl_path import *
from trex.stl.api import *


server = "10.1.5.42"
port = '8189'
order_no = time.strftime("%Y%m%d%H%M%S", time.localtime())
time_local = time.time()


def fetch_stats():
    c = STLClient(server=server)

    c.connect()
    c.acquire(ports=[0, 1], force=True)

    json_res = c.get_stats()
    print json_res['total']['ipackets']
    json_res['order_no'] = "trex"
    json_res['time'] = time_local
    # print json_res

    c.disconnect(stop_traffic=False)

    return json_res


while True:
    url = 'http://' + server + ':' + port + '/api/order/notify'
    json_res = fetch_stats()
    data = json.dumps(json_res)
    r = requests.post(url, data)
    msg = r.text
    print(msg)
    time.sleep(10)
