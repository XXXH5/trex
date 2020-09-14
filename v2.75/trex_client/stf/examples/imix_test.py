import os

from trex.examples.stl import stl_path
from trex.stl.api import *


def imix_test(server, mult):
    # create client
    c = STLClient(server=server)

    try:

        # connect to server
        c.connect()

        # take all the ports
        c.reset()

        # map ports - identify the routes
        table = stl_map_ports(c)
        # print(table)

        dir_0 = [x[0] for x in table['bi']]
        # dir_1 = [x[1] for x in table['bi']]

        # print("Mapped ports to sides {0} <--> {1}".format(dir_0, dir_1))

        # load IMIX profile
        profile = STLProfile.load_py(os.path.join(stl_path.STL_PROFILES_PATH, 'syn_attack.py'))
        streams = profile.get_streams()

        # add both streams to ports
        c.add_streams(streams, ports=dir_0)
        # c.add_streams(streams, ports = dir_1)

        # clear the stats before injecting
        c.clear_stats()

        # choose rate and start traffic for 10 seconds
        # duration = 10
        # print("Injecting {0} <--> {1} on total rate of '{2}' for {3} seconds".format(dir_0, dir_1, mult, duration))

        c.start(ports=(dir_0), mult=mult, total=True)

        if c.get_warnings():
            print("\n\n*** test had warnings ****\n\n")
            for w in c.get_warnings():
                print(w)
        print("Success start task on: {0}".format(server))
        return True

    except STLError as e:
        # passed = False
        print(e)
        return False

    finally:
        c.disconnect(stop_traffic=False)
