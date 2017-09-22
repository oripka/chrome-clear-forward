from scapy.all import *

def pkt_callback(pkt):
    pkt.show() # debug statement

sniff(iface="wlp2s0", prn=pkt_callback, filter="udp", store=0)
