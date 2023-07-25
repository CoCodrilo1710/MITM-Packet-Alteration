FROM snisioi/retele:2021

RUN apt-get update && apt-get install -y -qq iptables iproute2 libnetfilter-queue-dev net-tools bridge-utils build-essential

RUN pip3 install --upgrade python-iptables cython
RUN pip3 install scapy
RUN pip3 install NetfilterQueue

RUN mkdir -p /scripts
COPY src/*.sh /scripts/

COPY src/ManInTheMiddle.py /scripts

COPY src/tcp_client.py /scripts
COPY src/tcp_server.py /scripts
COPY src/TCP_Hijacker.py /scripts

COPY src/TCP_Hijack_Netfilter.py /scripts
