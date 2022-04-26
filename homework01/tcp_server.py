import socket
import sys

from tcp_thread import threaded

from _thread import *

import cache_control

CACHE_SIZE = 64

cache_control.cache_size = CACHE_SIZE
cache_control.cache = dict()
cache_control.cache_available = CACHE_SIZE

HOST = sys.argv[1]             #host
PORT = int(sys.argv[2])        #port
directory = sys.argv[3]        #path to save file

if directory[len(directory) - 1] != '/': directory += '/'
if directory == '.' or directory == './': directory = ''

# definições do socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print('\nsocket bind to port: %s' % (PORT))

# aguardando requisições
s.listen(5)
print("socket is listening")
print("set: 'ctrl + c' to kill server\n")

try:
    while True:
        # aceitando conexão com o client
        c, addr = s.accept()
        print('[port: %s] new connection with client' % (addr[1]))

        # a new thread client
        start_new_thread(threaded, (c, addr, directory))
except:
    pass
finally:
    print("SERVER OFF %s:%s" % (HOST, PORT))
    # close connection server
    s.close()