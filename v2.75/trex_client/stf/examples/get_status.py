from trex.stl.api import *
from pprint import pprint

def get_status(server):
    try:
        c = STLClient(server = server )
        c.connect()
        c.acquire(ports=[0,1], force = True)
        port_stats = c.get_stats()
        conn_info = c.get_connection_info()
        connection = "Server: "+conn_info['server'] + " sync_port: " + str(conn_info['sync_port'])
        
        server_version = c.get_server_version()
        server_version_fmt = "{0} @ {1}".format(server_version.get('mode', 'N/A'), server_version.get('version', 'N/A'))
        print(connection, server_version_fmt)
        c.acquire(ports=[0,1], force = True)
        
        cpu_util = port_stats['global']['cpu_util']
        # packet per second
        # total pps =  rx_pps
        total_pps = rx_pps = port_stats['total']['rx_pps']
        tx_pps = port_stats['total']['tx_pps']
        
        # byte per second
        # total bps = rx_bps
        total_bps = rx_bps = port_stats['total']['rx_bps']
        tx_bps = port_stats['total']['tx_bps']
        
        drop_rate = port_stats['global']['rx_drop_bps']
        res = {}
        res['server'] = conn_info['server']
        res['version'] = server_version_fmt
	res['cpu_util'] = round(cpu_util, 2)
	res['total_pps'] = round(total_pps, 2)
	res['tx_pps'] = round(tx_pps, 2)
	res['total_bps'] = round(rx_bps, 2)
	res['tx_bps'] = round(tx_bps, 2)
        res['drop_rate'] = round(drop_rate, 2)
	print(res)
        #pprint(res)
        if res:

            return res
    except Exception as e:
        print("Error has occurred during get stats:")
        print(e)
        return {}
    finally:
        #print(123)
        c.disconnect(stop_traffic=False)




