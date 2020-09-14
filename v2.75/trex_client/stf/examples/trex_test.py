# coding=utf-8


import json
import socket
import time
import csv


from test_path import *
from trex.stl.api import *
# trex
from trex_stf_lib.trex_client import CTRexClient
from trex_stf_lib.trex_status_e import TRexStatus

from get_active_hosts import get_active_host
# from trex.common.trex_client import TRexClient
from get_status import get_status
from imix_test import imix_test
from stop_traffic import stop_traffic
# configure python module path
from test_path import *

"""
get host local ip 
example:192.168.1.145
"""
REACHABLE_HOSTS_FILE = '/root/reachable_host.txt'


def save_reachable_hosts(ip_list):
    with open(REACHABLE_HOSTS_FILE, 'w') as f:
        for ip in ip_list:
            f.write(ip + '\n')


def read_reachable_host():
    ip_list = []
    with open(REACHABLE_HOSTS_FILE, 'r') as f:
        for line in f.readlines():
            ip_list.append(line.strip())
    return ip_list


def write_stats(stats, path):
    with open(path, "a") as f:
        f.write(stats)
    f.close()


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        return ip
    finally:
        s.close()


def start_stl_mode(ip):
    try:
        trex = CTRexClient(ip)
        if trex.get_running_status()['state'] == TRexStatus.Running:
            # print('server has already running')
            print('ip: ' + ip + ' server has started!')
        else:
            trex.start_stateless()
            time.sleep(1)  # 4
            if trex.get_running_status()['state'] == TRexStatus.Running:
                print("Success start, ip:" + ip)
        return True
    except Exception as e:
        print('\nError occurs when automatically starting up trex stateless server at: ' + ip + '\n')
        print(e)
        return False


def restart_stl_mode(ip):
    try:
        trex = CTRexClient(ip)
        if trex.get_running_status()['state'] == TRexStatus.Idle:
            # print('trex server process is not running')
            return False
        else:
            trex.force_kill(confirm=False)
            time.sleep(1)  # 4
            if trex.get_running_status()['state'] == TRexStatus.Idle:
                print("Success killed server, ip:" + ip)
                return True
    except Exception as e:
        print('Error occurred when automatically resetting up trex stateless server at: ' + ip)
        print(e)
        return False


def start_stl_test(ip):
    res = imix_test(ip, '30%')
    return res


def start_get_status(ip):
    res = get_status(ip)
    return res


def stop_stl_test(ip):
    res = stop_traffic(ip)
    return res


class TrexTest():
    def __init__(self, network, numbers):
        self.network = network
        self.numbers = numbers
        self.reachable_ip_list = []
        
        for i in range(4):
            ip = self.network + '.' + str(i+1)
            self.reachable_ip_list.extend(get_active_host(ip, self.numbers))
        print "Reachable hosts: {0}\n{1}".format(len(self.reachable_ip_list), self.reachable_ip_list)
        # print "Scanning reachable hosts:\n"
        #if os.path.isfile(REACHABLE_HOSTS_FILE):
        #    self.reachable_ip_list = read_reachable_host()
        #    print "Read from local file: ", self.reachable_ip_list
        #else:
        #self.reachable_ip_list = get_active_host(self.network, self.numbers)
        #save_reachable_hosts(self.reachable_ip_list)
        #print "Reachable hosts: {0}\n{1}".format(len(self.reachable_ip_list), self.reachable_ip_list)

        # print self.reachable_ip_list

        self.host_ip = get_host_ip()

        # self.remove_ip_from_list(host_ip)
        # reachable_ip_list.remove(gate_ways)

    # exit when there is no reachable host
    def check_server(self):
        ip_list = self.reachable_ip_list
        n = len(ip_list)
        if not n > 0:
            print 'Not enough server'
            return False
        return True

    def remove_ip_from_list(self, ip):
        self.reachable_ip_list.remove(ip)

    def auto_start_stl_mode(self):
        # remove ip on which occurred errors when starting
        print "Starting stl servers...\n"
        for i in self.reachable_ip_list:
            res = start_stl_mode(i)
            if not res:
                self.reachable_ip_list.remove(i)
                # print("Success start, ip:" + i)
        # print self.reachable_ip_list
        if self.reachable_ip_list > 0:
            print("TRex nodes with STL: {0} \n".format(len(self.reachable_ip_list)))
            # for i in host_started:
            #     print(i)

    def auto_reset_stl_mode(self):
        print "\nResetting stl servers...\n"
        check = self.check_server()
        if not check:
            return False
        host_killed = []
        for i in self.reachable_ip_list[:len(self.reachable_ip_list)]:
            if restart_stl_mode(i):
                host_killed.append(i)
            elif not restart_stl_mode(i):
                print('Failed to kill server on {0}: server was not running'.format(i))
        if (len(host_killed)) > 0:
            print("TRex nodes has been killed: {0} \n".format(len(host_killed)))
            # for i in host_killed:
            #     print('ip: ' + i)

    """
        traffic profile: stl/syn_attack.py
    """

    def auto_start_stl_test(self):
        print "\nStarting traffic...\n"
        check = self.check_server()
        if not check:
            return False

        host_started = []
        for i in self.reachable_ip_list[:len(self.reachable_ip_list)]:
            if start_stl_test(i):
                host_started.append(i)
                # print("Success start, ip:" + i)

        if len(host_started) > 0:
            print("TRex nodes with traffic started: {0} \n".format(len(host_started)))
            # for i in host_started:
            #     print(i)

    def auto_get_status(self, path):
        # path = '/root/result.txt'
        check = self.check_server()
        if not check:
            return False

        host_started = []
        # 创建新的测试结果文件
        final_result = {'total_nodes': 0, 'total_bps': 0, 'total_pps': 0, 'aver_bps': 0, 'aver_pps': 0,
                        'aver_cpu_utils': 0}
        # 循环获取每个节点的状态数据，并保存到结果文件中
        for i in self.reachable_ip_list[:len(self.reachable_ip_list)]:
            stats = start_get_status(i)
            if stats:
                print("Success got stats on: {0} \n".format(i))
                write_stats(json.dumps(stats), path)
                #     total_bps, total_pps
                final_result['total_bps'] += stats['total_bps']
                final_result['total_pps'] += stats['total_pps']
                final_result['aver_cpu_utils'] += stats['cpu_util']  # 先把所有的cpu利用率加起来
                host_started.append(i)
                # print("Success start, ip:" + i)
            else:
                print("Failed got stats on:" + i)

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
        final_result['total_nodes'] = success_nodes
        final_result['aver_bps'] = round(final_result['total_bps'] / success_nodes, 2)
        final_result['aver_pps'] = round(final_result['total_pps'] / success_nodes, 2)
        final_result['aver_cpu_utils'] = round(final_result['aver_cpu_utils'] / success_nodes, 2)
        write_stats(json.dumps(final_result), path)

        if len(host_started) > 0:
            print("TRex nodes success got status: {0} \n".format(len(host_started)))
            # for i in host_started:
            #     print(i)
    
    
    def auto_get_status_to_csv(self, writer):
        # path = '/root/result.txt'
        check = self.check_server()
        if not check:
            sys.exit(1)

        host_started = []
        # 创建新的测试结果文件
        final_result = {'total_nodes': 0, 'total_bps': 0, 'total_pps': 0, 'aver_bps': 0, 'aver_pps': 0,
                        'aver_cpu_utils': 0}
        # 循环获取每个节点的状态数据，并保存到结果文件中
        for i in self.reachable_ip_list[:len(self.reachable_ip_list)]:
            stats = start_get_status(i)
            if stats:
                print("Success got stats on: {0} \n".format(i))
                writer.writerow((stats['server'], stats['version'], stats['cpu_util'], stats['total_pps'],
                                 stats['total_bps'], stats['tx_pps'], stats['tx_bps'], stats['drop_rate']))
                # total_bps, total_pps
                final_result['total_bps'] += stats['total_bps']
                final_result['total_pps'] += stats['total_pps']
                final_result['aver_cpu_utils'] += stats['cpu_util']  # 先把所有的cpu利用率加起来
                host_started.append(i)
                # print("Success start, ip:" + i)
            else:
                print("Failed got stats on:" + i)

        success_nodes = len(host_started)

        # 对数据进行处理
        """
        average_cput_utils
        average_bps
        average_pps

        drop_node: ip
            drop_rate:
        """
        final_result['total_nodes'] = success_nodes
        final_result['aver_bps'] = round(final_result['total_bps'] / success_nodes, 2)
        final_result['aver_pps'] = round(final_result['total_pps'] / success_nodes, 2)
        final_result['aver_cpu_utils'] = round(final_result['aver_cpu_utils'] / success_nodes, 2)
        # write_stats(json.dumps(final_result), path)
        writer.writerow(" ")
        writer.writerow(("Total Nodes", " ", "Average CPU Utils", "Total PPS", "Total BPS",
                         "Average PPS", "Average BPS", " "))
        writer.writerow((final_result['total_nodes']," ", final_result['aver_cpu_utils'], final_result['total_pps'],
                         final_result['total_bps'], final_result['aver_pps'], final_result['aver_bps'], " "))
        writer.writerow(" ")
        if len(host_started) > 0:
            print("TRex nodes success got status: {0} \n".format(len(host_started)))    
    
    def monitor(self):
        print "\nGetting stats...\n"
        # ips = self.reachable_ip_list
        path = "/root/result.txt"
        # localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open(path, "w") as f:
            f.write("\n#################### TEST DATA ####################\n")
        for i in range(3):
            with open(path, "a") as f:
                f.write("\n-------------------- TEST {0} --------------------\n".format(i + 1))
            self.auto_get_status(path)
            time.sleep(10)
        f.close()


    def loop_test(self):
        print "Starting loop test..."
        path = "/root/loop_test_result.csv"
        csv_file = open(path, 'w')
        writer = csv.writer(csv_file)
        try:
            for i in range(3):
                writer.writerow(
                    ('sever', 'version', 'cpu_util', 'total_pps', 'total_bps', 'tx_pps', 'tx_bps', 'drop_rate'))
                self.auto_get_status_to_csv(writer)
                time.sleep(10)
        finally:
            csv_file.close()


    
    def auto_stop_traffic(self):
        print "\nStopping traffic..."
        check = self.check_server()
        if not check:
            return False
        host_killed = []
        for i in self.reachable_ip_list[:len(self.reachable_ip_list)]:
            if stop_stl_test(i):
                host_killed.append(i)
        if (len(host_killed)) > 0:
            print("TRex nodes success stopped traffic: {0} \n".format(len(host_killed)))
            # for i in host_killed:
            #     print('ip: ' + i)
