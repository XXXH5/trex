import time
import datetime
from examples.stf_path import *
from trex_stf_lib.trex_client import CTRexClient


from get_active_hosts import get_active_host
from trex_stf_lib.trex_status_e import TRexStatus
from imix_test import imix_test
def start_stl_test(ip):
    imix_test(ip, '30%')

def auto_start_stl_test(ip_list, n=None):
    if not n:
        n = len(ip_list)
    host_started = []
    for i in ip_list[:n]:
        if start_stl_test(i):
            host_started.append(i)
            #print("Success start, ip:" + i)
            
    if len(host_started)>0:
        print("trex nodes with STL: {0}".format(len(host_started)))            
        for i in host_started:
            print(i)
        
        
if __name__ == '__main__':
    network = '192.168.1'
    n = 130
    print('Scanning reachable ips...')
    ips = get_active_host(network, n)
    #ips.remove("192.168.115.1")
    #ips.remove('192.168.115.2')
    #ips.remove('192.168.115.129')
    ips.remove("192.168.1.30")
    print('Results:',ips)
    print('Starting stateless trex test on these ips')
    auto_start_stl_test(ips)
 
