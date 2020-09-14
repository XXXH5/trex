#!/usr/bin/python2
import multiprocessing
import subprocess
import os


def ping( job_q, results_q ):
    DEVNULL = open(os.devnull,'w')
    while True:
        ip = job_q.get()
        if ip is None: break

        try:
            subprocess.check_call(['ping', '-c1', ip],
                                  stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass


def get_active_host(network, n):
    ret = []
    pool_size = n
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [multiprocessing.Process(target=ping, args=(jobs, results)) for i in range(pool_size)]

    for p in pool:
        p.start()

    for i in range(1, n+1):
        jobs.put(network + '.' + str(i))  # bydefault scans for network 192.168.1.1-255

    for p in pool:
        jobs.put(None)

    for p in pool:
        p.join()
    
    
    while not results.empty():
        ip = results.get()
        ret.append(ip)
    
    return ret



if __name__ == '__main__':
    for i in range(4):
        ips = get_active_host('192.168.'+str(i+1), 100)
        print(len(ips))
        print(ips)
