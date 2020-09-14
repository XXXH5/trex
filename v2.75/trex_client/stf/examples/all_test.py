# coding=utf-8
import time

from trex_test import TrexTest

t1 = time.time()
new_test_1 = TrexTest('192.168', numbers=60)
#new_test_2 = TrexTest('192.168.2', numbers=60)
#new_test_3 = TrexTest('192.168.3', numbers=60)
#new_test_4 = TrexTest('192.168.4', numbers=60)

# remove gateway from reachable host list, if necessary remove host ip
# manager
#new_test_1.remove_ip_from_list('192.168.1.8')
#new_test_2.remove_ip_from_list('192.168.2.8')
#new_test_3.remove_ip_from_list('192.168.3.9')
#new_test_4.remove_ip_from_list('192.168.4.8')

new_test_1.remove_ip_from_list('192.168.1.8')
new_test_1.remove_ip_from_list('192.168.2.8')
new_test_1.remove_ip_from_list('192.168.3.9')
new_test_1.remove_ip_from_list('192.168.4.8')







# First reset trex daemon server
#new_test.auto_reset_stl_mode()

# Second start trex daemon server in staeless mode 
new_test_1.auto_start_stl_mode()

# Third start traffic on server
new_test_1.auto_start_stl_test()
time.sleep(10)

# Fourth wait 10s and get stats from server 
#new_test.monitor()
new_test_1.loop_test()


# Last stop the running traffic on server 
new_test_1.auto_stop_traffic()
t2 = time.time()
print "Test has lasted {0} seconds since task started!".format(str(t2 - t1))
