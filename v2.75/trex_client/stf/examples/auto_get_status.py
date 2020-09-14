# coding=utf-8
import time
import datetime
from examples.stf_path import *
from trex_stf_lib.trex_client import CTRexClient
import json

from get_active_hosts import get_active_host
from trex_stf_lib.trex_status_e import TRexStatus
from imix_test import imix_test
from get_status import get_status

# def process_stats_data(stats):
#     stats_processed
#     return stats_processed
#

def write_stats(stats, path):
    with open(path, "a") as f:
        f.write(stats)
    f.close()


def start_get_status(ip):
    res = get_status(ip)
    return res


def auto_start_get_status(ip_list, path, n=None):
    if not n:
        n = len(ip_list)
    host_started = []
    # 创建新的测试结果文件
    final_result = {'total_nodes': 0, 'total_bps':0, 'total_pps':0, 'aver_bps':0, 'aver_pps':0, 'aver_cpu_utils':0 }
    # 循环获取每个节点的状态数据，并保存到结果文件中
    for i in ip_list[:n]:
        stats = start_get_status(i)
        if stats:
            print("sucess get stats on Server :" + i)
            write_stats(json.dumps(stats),path)
            #     total_bps, total_pps
            final_result['total_bps'] += stats['total_bps']
            final_result['total_pps'] += stats['total_pps']
            final_result['aver_cpu_utils'] += stats['cpu_util']   # 先把所有的cpu利用率加起来
            host_started.append(i)
            #print("Success start, ip:" + i)
        else:
            print("fail get stats on Server :" + i)

    success_nodes = len(host_started)

    # 对数据进行处理
    """
    average_cput_utils
    average_bps
    average_pps

    drop_node: ip
        drop_rate:
    """
    write_stats("\n******************RESULT********************\n", path)
    final_result['total_nodes']  = success_nodes
    final_result['aver_bps'] = round(final_result['total_bps']/success_nodes, 2)
    final_result['aver_pps'] = round(final_result['total_pps']/success_nodes, 2)
    final_result['aver_cpu_utils'] = round(final_result['aver_cpu_utils']/success_nodes, 2)
    write_stats(json.dumps(final_result),path)


    if len(host_started)>0:
        print("number of success get in trex nodes: {0}".format(len(host_started)))
        for i in host_started:
            print(i)

def monitor(ips):
    path = "/root/result.txt"
    with open(path, "w") as f:
        f.write("#################### TEST DATA ####################\n")
    for i in range(2):
    	with open(path, "a") as f:     
		f.write("\n-------------------- TEST {0} --------------------\n".format(i+1))
        auto_start_get_status(ips, path)
        time.sleep(10)



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
    print('Starting get status on these ips')
    monitor(ips)


