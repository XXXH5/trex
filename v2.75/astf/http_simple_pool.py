from trex.astf.api import *


class Prof1():
    def __init__(self):
        pass

    def get_profile(self, **kwargs):
        # ip generator
        ip_gen_c = ASTFIPGenDist(ip_range=["1.1.1.1", "1.1.1.1"], distribution="seq")
        ip_gen_s = ASTFIPGenDist(ip_range=["2.2.2.2", "2.2.2.2"], distribution="seq")
        ip_gen = ASTFIPGen(glob=ASTFIPGenGlobal(ip_offset="1.0.0.0"),
                           dist_client=ip_gen_c,
                           dist_server=ip_gen_s)

        return ASTFProfile(default_ip_gen=ip_gen,
                           cap_list=[ASTFCapInfo(file="../avl/delay_10_dns_0.pcap", cps=1),
                                     ASTFCapInfo(file="../avl/delay_10_dns_0.pcap", cps=1,port=111)],
                        )


def register():
    return Prof1()

