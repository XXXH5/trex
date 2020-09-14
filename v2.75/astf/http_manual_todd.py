# Example for creating your program by specifying buffers to send, without relaying on pcap file

from trex.astf.api import *


class Prof1():
    def __init__(self):
        pass  # tunables


    def _udp1400(self, **kwargs):

        random.seed = 10
        payload_size = 1400
        payload = "".join([string.ascii_letters[int(
            random.random() * len(string.ascii_letters))] for i in range(payload_size)])

        if not kwargs['rate']:

            print("Rate is recommended for udp profile...setting to 500 Mbps")

            mbit_rate = 500 * 1000 * 1000

        else:

            mbit_rate = int(kwargs['rate'])

        pps_rate = mbit_rate / ((50 + payload_size) * 8) / 2

        pps_rate_client = pps_rate / int(kwargs['limit'])

        usec_delay = int(1000000 / pps_rate_client)

        print("mbit_rate: %d, pps_rate: %d, pps_rate_client: %d, usec_delay: %d" % (
            mbit_rate, pps_rate, pps_rate_client, usec_delay))

        # client commands

        prog_c = ASTFProgram(stream=False)

        prog_c.send_msg(payload)

        prog_c.set_var("var3", 1000000)

        prog_c.set_label("b:")

        prog_c.send_msg(payload)

        prog_c.delay(usec_delay)

        prog_c.jmp_nz("var3", "b:")

        # server commands

        prog_s = ASTFProgram(stream=False)

        prog_s.recv_msg(1)

        prog_s.set_var("var2", 1000000)

        prog_s.set_label("a:")

        prog_s.send_msg(payload)

        prog_s.delay(usec_delay)

        prog_s.jmp_nz("var2", "a:")

        info = ASTFGlobalInfo()

        return {'prog_c': prog_c, 'prog_s': prog_s, 'info': info}

    def create_profile(self):

        p = self._udp1400(rate=6000000000, limit=800)

        # ip generator
        ip_gen_c = ASTFIPGenDist(
            ip_range=["16.0.0.1", "16.0.0.255"], distribution="rand")
        ip_gen_s = ASTFIPGenDist(
            ip_range=["48.0.0.1", "48.0.0.255"], distribution="rand")

        ip_gen = ASTFIPGen(glob=ASTFIPGenGlobal(ip_offset="1.0.0.0"),
                        dist_client=ip_gen_c, dist_server=ip_gen_s)

        info = p['info']
        #template
        temp_c = ASTFTCPClientTemplate(program=p['prog_c'], ip_gen=ip_gen, port=80)
        temp_s = ASTFTCPServerTemplate(
            program=p['prog_s'], assoc=ASTFAssociationRule(port=80))

        template = ASTFTemplate(client_template=temp_c, server_template=temp_s)

        # profile
        profile = ASTFProfile(default_ip_gen=ip_gen, templates=template,
                            default_c_glob_info=info, default_s_glob_info=info)
        return profile


    def get_profile(self, **kwargs):
        return self.create_profile()


def register():
    return Prof1()
