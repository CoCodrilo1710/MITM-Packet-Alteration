# TCP Server
import socket
import logging
import random

logging.basicConfig(format=u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.NOTSET)
allowed_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)

port = 50001
address = '198.7.0.2'
server_address = (address, port)
sock.bind(server_address)
logging.info("Server started on %s and port %d", address, port)
max_length = 5

sock.listen(1)

try:
    while True:
        logging.info('Waiting for connections...')
        connection, address = sock.accept()
        logging.info("Handshake with %s", address)
        print()
        print("Handshake with %s", address)

        while True:
            data = connection.recv(1024).decode('utf-8')
            if not data:
                connection.close()
                break
            print()
            print('Received content: "%s"' % data)
            print()
            message = 'From server ' + ''.join(random.choice(allowed_characters) for i in range(random.randint(1, max_length)))
            print('Sending message: "%s"' % message)
            connection.sendall(message.encode('utf-8'))
            print()

except:
    sock.close()
