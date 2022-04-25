# thread para instancia do client

import pickle
from time import sleep
import file_control

BUFFER_SIZE = 1024

def threaded(c, addr, directory):
    # variaveis globais
    global cache
    global cache_available
    global locked

    # recebendo a request do client
    data = c.recv(BUFFER_SIZE)
    # deserializando a request
    res = pickle.loads(data)

    print("[port: %s] client is requesting file '%s'" % (
        addr[1], res))

    # check if file exists in the directory or cache
    if file_control.isExist(directory + res):
        # checks if file is larger than the cache
        print("[port: %s] sending file '%s' to client" % (addr[1], res))
        # prepares client to receive file
        package = pickle.dumps(True)
        c.send(package)

        # serialization of the file for sending
        with open(directory + res, 'rb') as f:
            package = f.read(BUFFER_SIZE)
            while package:
                # sending file packages
                c.send(package)
                package = f.read(BUFFER_SIZE)
            sleep(1)
            f.close()

        print("[port: %s] sent file '%s'" % (
                    addr[1], res))
        # if file does not exist
    else:
        print("[port: %s] file '%s' not found" % (addr[1], res))
        # warns that file does not exist
        package = pickle.dumps(False)
        c.send(package)

    print("[port: %s] closed connection with client" % (addr[1]))
    c.close()