# TCP client
import socket
import logging
import time
import random

allowed_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

logging.basicConfig(format=u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)

port = 50001
address = '198.7.0.2'
server_address = (address, port)
max_length = 3

try:
    logging.info('Handshake with %s', str(server_address))
    print("Handshake with %s", str(server_address))
    sock.connect(server_address)
    while True:
        message = 'From client ' + ''.join(random.choice(allowed_characters) for i in range(random.randint(1, max_length)))

        sock.sendall(message.encode('utf-8'))
        data = sock.recv(1024).decode('utf-8')
        if not data:
            break

        print(f"Sending message: {message}")
        print()
        print(f"Received content: {data}")
        print()
        print()
        time.sleep(1)

finally:
    logging.info('closing socket')
    print('closing socket')
    sock.close()
