from scapy.all import *
from datetime import datetime
import time
import datetime
import sys

# Select interface and ports of interest
interface = 'ens33'
bpf = 'udp and port 53'

# SELECT/FILTER MSGS
def select_DNS(pkt):
    pkt_time = pkt.sprintf('%sent.time%')


# SELECT/FILTER DNS MSGS
    try:

        dict = []

        # queries
        if DNSQR in pkt and pkt.dport == 53:
            domain = pkt.getlayer(DNS).qd.qname.decode() # .decode() gets rid of the b''
            print('Q - Time: ' + pkt_time + ' , source IP: ' + pkt[IP].src + ' , domain: ' + domain)

        # responses
        elif DNSRR in pkt and pkt.sport == 53:
            domain = pkt.getlayer(DNS).qd.qname.decode()
            print('R - Time: ' + pkt_time + ' , source IP: ' + pkt[IP].src + ' , domain: ' + domain)

    except:
        pass

# START SNIFFER
sniff(iface=interface, filter=bpf, store=0,  prn=select_DNS)