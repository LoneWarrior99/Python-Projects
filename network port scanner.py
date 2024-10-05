from scapy.all import ARP, Ether, srp
from argparse import ArgumentParser
import socket
from queue import Queue
from threading import Thread, Lock

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
    worker = q.qet()
    #scan port number
    open_port(worker)
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
  prog='Network Port Scanner'
  description='This is a basic network scanner using arp requests'
  epilog='Thanks for looking!'
)

#set up help menu
parser.add_argument('-t', "--target", help="Use the syntax -t to specify your target. Must be in CIDR Notation", required=True)

#pareses command line arguements
args = parser.parse_args()

#Change target to IP you want to scan
target_ip = args.target

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

answer = input("Enter number\n")

if answer == "1":
  host = input("Enter the host:")
  print ("What ports would are you looking to scan?")
  ports = input("Enter the ports/range:")
  host, port_range = host,ports

  start_port, end_port = port_ranges.split("-")
  start_port, end_port = int(start_port),int(end_port)

  ports = [ p for p in range(start_port, end_port)]

  main(host, ports)

  print("Scan Complete")

else:
  print("Goodbye!")


