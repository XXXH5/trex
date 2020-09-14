from trex.stl.api import *

def stop_traffic(server):
    try:
        c = STLClient(server = server )
        c.connect()
        c.acquire(ports=[0,1], force = True)
        c.stop()
        # check port status transmitting
        print('Success stop traffic on server :' +server)
        return True
    except Exception as e:
        print("Error has occurred during stopping stats:")
        print(e)
        return False
    finally:
        c.disconnect()
