# MITM-Packet-Alteration

## Instructions & Docs

This app use the TCP Hijack technique improved with continuously packet injection with different lengths compared to the initial message. Works with help of ARP Spoofing in order to get the messages through the attacker's machine, but after succesfully redirect the packets, the script use a custom dictionary in order to save the ack and seq numbers of the original packets and alter them for client->server way of sending. 

If I would like to alter the original payload with a payload with the same length, the dictionary would not be necessary, a simple modification of the payload associated with the packet would be enough.

Like the ARP Spoofing repo, this repo is also using a docker container to get done the job. The docker file is found in the 'docker' folder and the source code and auxiliary files are found in the 'src' folder. 

To see if this attack works, look at the tcp_server.py output, the sent messages will not coresspond with the received ones.
