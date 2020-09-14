import time
import datetime
from examples.stf_path import *
from trex_stf_lib.trex_client import CTRexClient

from get_active_hosts import get_active_host
from trex_stf_lib.trex_status_e import TRexStatus
from stop_traffic import stop_traffic

def stop_traffic_single(ip):
    res = stop_traffic(ip)
    return res

def auto_stop_traffic(ip_list, n=None):
    if not n:
        n = len(ip_list)
    host_killed = []
    for i in ip_list[:n]:
        if stop_traffic_single(i):
            host_killed.append(i)
    if (len(host_killed)) > 0:
        print("trex tasks has been stopped: {0}".format(len(host_killed)))
        for i in host_killed:
            print('ip: ' + i)


if __name__ == '__main__':
    network = '192.168.1'
    n = 100
    print('Scanning reachable ips')
    ips = get_active_host(network, n)
    # filter gateways
    #ips.remove("192.168.115.1")
    #ips.remove("192.168.115.2")
    #ips.remove("192.168.115.129")
    ips.remove("192.168.1.30")
    # show the result ips
    print(ips)
    # start statelesss servers
    auto_stop_traffic(ips)
# restart_daemon_server('192.168.115.130')
