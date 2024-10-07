from scapy.all import *
from argparse import ArgumentParser
import socket
from queue import Queue
from threading import Thread, Lock
import ipinfo
import time
import pyfiglet
from datetime import datetime


#pretty title
ascii_banner = pyfiglet.figlet_format("NETWORK SCANNER")
print(ascii_banner)



#Change to increase or decrease speed
N_THREADS = 200
q = Queue()
print_lock = Lock()

def open_ports(port):
  """
  This will determine if the host has the port open or closed
  """

  try:
    s = socket.socket()
    #tries to connect to the host using that port
    s.connect((host, port))

  except:
    with print_lock:
    #cant connect to port mean its closed  
    
      return False
  else:
    #connection established mean port is open
    with print_lock:
      print(f"{host:15}:{port:5} is open ")

  finally:
      s.close()


def scan_thread():
  global q
  while True:
    #get the port number from the queue
    worker = q.get()
    #scan port number
    open_ports(worker)
    #tells it when finished
    q.task_done()

def main (hosts, ports):
  global q 
  for t in range (N_THREADS):
    t = Thread(target=scan_thread)
    #when daemon set to true the thread will end when main thread ends
    t.daemon = True
    t.start()
  for worker in ports:
    #puts ports in queue
    q.put(worker)

  q.join()




parser = ArgumentParser(
  prog='Network Scanner',
  description='This is a network scanner using arp requests with additonal port scans, geolocater, and dhcp listener.',
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
  clients.append({ 'ip': received.psrc, 'mac': received.hwsrc})


#prints clients
print("Available devices in the network:")
print("IP" + " "*18+"MAC")
for client in clients:
  print("{:16}    {}".format(client['ip'], client['mac']))


print("What now?")
print("1.Port Scan")
print("2.GELOCATE IP")
print("3.DHCP Listener")

answer = input("Enter number\n")


if answer == "1":
  host = input("Enter the host:")
  print ("What ports would are you looking to scan?")
  ports = input("Enter the ports/range:")
  host, port_range = host,ports

  start_port, end_port = port_range.split("-")
  start_port, end_port = int(start_port),int(end_port)

  ports = [ p for p in range(start_port, end_port)]

  main(host, ports)

  print("Scan Completed")


if answer == "2":
  print("What IP would you like to geolocate?")
  geotarget = input()
  #IPINFO access token
  access_token ='123456789'

  handler = ipinfo.getHandler(access_token)
  details = handler.getDetails(geotarget)

  for key, value in details.all.items():
    print(f"{key}: {value}")
  

if answer == "3":
  print("Listening...")
  
  def dhcp_listener():
    #set Up BPF filter
    sniff (prn=print_packet, filter='udp and (port 67 or port 68)')

  def print_packet(packet):
    target_mac, requested_ip, hostname, vendor_id = [None] *4
    #get mac address from packet
    if packet.haslayer(Ether):
      target_mac = packet.getlayer(Ether).src
      # get DHCP options
    dhcp_options = packet[DHCP].options
    for item in dhcp_options:
      try:
        label, value =item
      except ValueError:
        continue
      if label == "requested_addr":
        requested_ip = value
      
      elif label == "hostname":
        hostname = value.decode()

      elif label == "vendor_class_id":
        vendor_id = value.decode()

    if target_mac and vendor_id and hostname and requested_ip:
      #prints all if the variable arent blank
      time_now = time.strftime("[%Y-%m-%d - %H:%M:%S]")
      print(f"{time_now} : {target_mac} - {hostname} / {vendor_id} requested {requested_ip}")

  dhcp_listener()
  



else:
  print("Goodbye!")
