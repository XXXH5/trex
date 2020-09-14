import time
import datetime
from examples.stf_path import *
from trex_stf_lib.trex_client import CTRexClient


from get_active_hosts import get_active_host
from trex_stf_lib.trex_status_e import TRexStatus
def start_stl_mode(ip):
    try:
        trex = CTRexClient(ip)
        if trex.get_running_status()['state'] == TRexStatus.Running:
            #print('server has already running')
            print('ip: '+ ip +' server has started!')
            return False
        else:
            trex.start_stateless()
            #time.sleep(2)  # 4
            if trex.get_running_status()['state'] == TRexStatus.Running:
                print("Success start, ip:" + ip)
                return True
    except Exception as e:
        print('\nerror occurs when automatically starting up trex stateless server at: ' + ip +'\n')
        print(e)
        pass

def auto_start_stl_mode(ip_list, n=None):
    if not n:
        n = len(ip_list)
    host_started = []
    for i in ip_list[:n]:
        if start_stl_mode(i):
            host_started.append(i)
            #print("Success start, ip:" + i)
            
    if len(host_started)>0:
        print("trex nodes with STL: {0}".format(len(host_started)))            
        for i in host_started:
            print(i)
        
        
if __name__ == '__main__':
    network = '192.168.1'
    n = 100
    print('Scanning reachable ips...')
    ips = get_active_host(network, n)
    #ips.remove("192.168.115.1")
    #ips.remove('192.168.115.2')
    #ips.remove('192.168.115.129')
    ips.remove("192.168.1.30")
    print('Results:',ips)
    print('Starting stateless trex server on these ips')
    auto_start_stl_mode(ips)
    

