from trex.astf.api import *


class Prof1():
    def __init__(self):
        pass  # tunables

    def http1b_t(self):

        http_req = 'GET /450 HTTP/1.1\r\nHost: 10.6.1.1\r\nConnection: close\r\nUser-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1) Opera 8.0\r\nAccept: */*\r\nAccept-Language: en-us\r\nAccept-Encoding: gzip, deflate, compress\r\n\r\n'
        http_response = 'HTTP/1.1 200 OK\r\nServer: Jetty/4.2.9rc2 (SunOS/5.8 sparc java/1.4.1_04)\r\nContent-Type: text/html\r\nConnection: close\r\nContent-Length: 11000\r\n\r\n'
        http_response2 = '*'
        http_total_response = http_response + http_response2

        # client commands

        prog_c = ASTFProgram()
        prog_c.connect();
        prog_c.send(http_req)
        prog_c.recv(len(http_total_response))
        prog_c.delay(10);

    

        prog_s = ASTFProgram()
        prog_s.recv(len(http_req))
        prog_s.delay(10);
        prog_s.send(http_total_response)
        prog_s.wait_for_peer_close()

    

        # ip generator

        ip_gen_c = ASTFIPGenDist(ip_range=["12.2.0.1", "12.2.0.255"], distribution="rand")

        ip_gen_s = ASTFIPGenDist(ip_range=["10.11.0.3", "10.11.0.5"], distribution="rand")

        ip_gen = ASTFIPGen(glob=ASTFIPGenGlobal(ip_offset="1.0.0.0"),dist_client=ip_gen_c,dist_server=ip_gen_s)

        ip_gen_c = ASTFIPGenDist(ip_range=["12.1.0.1", "12.1.0.255"], distribution="rand")

        ip_gen_s = ASTFIPGenDist(ip_range=["10.10.0.3", "10.10.0.5"], distribution="rand")

        ip_gen2 = ASTFIPGen(glob=ASTFIPGenGlobal(ip_offset="1.0.0.0"),dist_client=ip_gen_c,dist_server=ip_gen_s)

        info = ASTFGlobalInfo()

        info.tcp.mss = 1100

        info.tcp.rxbufsize = 1102  # split the buffer to MSS and ack every buffer, no need the no_delay option

        info.tcp.txbufsize = 1100

        info.tcp.initwnd = 1

        info.tcp.delay_ack_msec = 20

        #info.tcp.no_delay = 1

        info.tcp.do_rfc1323 =0

        info.scheduler.rampup_sec = 30

        #template

        temp_c1 = ASTFTCPClientTemplate(program=prog_c, ip_gen=ip_gen, port=81)

        temp_c2 = ASTFTCPClientTemplate(program=prog_c, ip_gen=ip_gen2, port=81)

        temp_s = ASTFTCPServerTemplate(program=prog_s,assoc=ASTFAssociationRule(port=81))

    #    temp_c = ASTFTCPClientTemplate(program=prog_c, ip_gen=ip_gen)

    #    temp_s = ASTFTCPServerTemplate(program=prog_s)

    

        template1 = ASTFTemplate(client_template=temp_c1, server_template=temp_s)

        template2 = ASTFTemplate(client_template=temp_c2, server_template=temp_s)

        # profile

        profile = ASTFProfile(default_ip_gen=ip_gen, templates = [template1,template2], default_c_glob_info=info, default_s_glob_info=info)

        return profile

    def get_profile(self, **kwargs):
        return self.http1b_t()
 
def register():
    return Prof1()
