from scapy.all import ARP, Ether, srp
from argparse import ArgumentParser
import pyfiglet
from datetime import datetime


#pretty title
ascii_banner = pyfiglet.figlet_format("arp network scanner")
print(ascii_banner)



parser = ArgumentParser(
  prog='Network Scanner',
  description='This is a basic network scanner using arp requests',
  epilog='Thanks for looking!'
)

#set up help menu
parser.add_argument('-t', "--target", help="Use the syntax -t to specify your target. Must be in CIDR Notation", required=True)

#pareses command line arguements
args = parser.parse_args()

#Change target to IP you want to scan
target_ip = args.target

#Banner 
print("_" *50)
print("Scanning Targets: " + target_ip)
print("Scanning started at: " + str(datetime.now()))
print("_" *50)


#Create arp packet
arp = ARP(pdst=target_ip)

#Create ether broadcast packet
ether = Ether(dst='ff:ff:ff:ff:ff:ff')
packet = ether/arp
#This stacks them

result = srp(packet, timeout=3, verbose=0)[0]

#list of clients
clients = []

for sent, received in result:
  #for each respond, append ip and mac to clients list
  clients.append({'ip': received.psrc, 'mac': received.hwsrc})



#prints clients
print("Available devices in the network:")
print("IP" + " "*18+"MAC")
for client in clients:
  print("{:16}    {}".format(client['ip'], client['mac']))
  
