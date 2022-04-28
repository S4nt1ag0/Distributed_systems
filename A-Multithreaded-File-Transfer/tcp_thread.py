# thread para instancia do client

import pickle

from filelock import FileLock
from time import sleep

import file_control
import cache_control
import lock_control

BUFFER_SIZE = 1024

def threaded(clientSocket, addr, directory):
    # variaveis globais

    # recebendo a request do client
    data = clientSocket.recv(BUFFER_SIZE)
    # deserializando a request
    res = pickle.loads(data)
    if res == 'list':
        print("[port: %s] checking files on cache" % (addr[1]))
        if len(cache_control.cache) == 0:
            clientSocket.send(pickle.dumps('cache is empty'))
        else:
            package = '\nFiles on cache:\n\n'
            for file in cache_control.cache.keys():
                package += file + '\n'
            clientSocket.send(pickle.dumps(package))

            print("[port: %s] list files on cache sended to client" % (addr[1]))
    else:
        print("[port: %s] client is requesting file '%s'" % (
            addr[1], res))
        # ativando o lock
        lock_control.lock.acquire()

        # check if file exists in the directory or cache
        if file_control.isExist(directory + res) or res in cache_control.cache:
            # checks if file is larger than the cache
            if file_control.getFile_size(directory + res) > cache_control.cache_size and res not in cache_control.cache:
                print("[port: %s] sending file '%s' to client" % (addr[1], res))
                # prepares client to receive file
                package = pickle.dumps(True)
                clientSocket.send(package)

                # serialization of the file for sending
                with FileLock(directory + res + '.lock'):
                    with open(directory + res, 'rb') as f:
                        package = f.read(BUFFER_SIZE)
                        while package:
                            # sending file packages
                            clientSocket.send(package)
                            package = f.read(BUFFER_SIZE)
                        sleep(1)
                        f.close()

                print("[port: %s] sent file '%s'" % (
                            addr[1], res))
            else:
                # check if file exists in cache
                if res not in cache_control.cache:

                    print("[port: %s] add file '%s' on cache" % (
                        addr[1], res))
                    size_file = file_control.getFile_size(directory + res)

                    # free up cache space
                    if cache_control.cache_available < size_file:
                        for key_file in list(cache_control.cache):
                            # remove file from cache
                            if not cache_control.cache[key_file][2]: #verificando se o arquivo não esta com lock
                                print("[port: %s] remove a file '%s' by cache" % (
                                    addr[1], key_file))
                                file_removed = cache_control.cache.pop(key_file)
                                file_removed_size = file_removed[0]
                                cache_control.cache_available += file_removed_size

                    # serialize file
                    packages = []
                    with open(directory + res, 'rb') as f:
                        package = f.read(BUFFER_SIZE)
                        while package:
                            packages.append(package)
                            package = f.read(BUFFER_SIZE)
                        sleep(1)
                        f.close()

                    # add file to cache
                    cache_control.cache[res] = [size_file, packages, True]
                    cache_control.cache_available -= size_file

                    print("[port: %s] file '%s' on cache" % (addr[1], res))

                # block cache file
                cache_control.cache[res][2] = True

                # query cache file to be sent
                file_in_cache = cache_control.cache[res]
                size_file = file_in_cache[0]
                packages = file_in_cache[1]

                # flush file from cache
                cache_control.cache[res][2] = False

                # -------
                # sending through the cache
                print("[port: %s] sending file '%s' to client through the cache" % (
                    addr[1], res))
                package = pickle.dumps(True)
                clientSocket.send(package)

                for package in packages:
                    clientSocket.send(package)
                sleep(1)
                print("[port: %s] sent file '%s' to client" % (
                    addr[1], res))
        # if file does not exist
        else:
            print("[port: %s] file '%s' not found" % (addr[1], res))
            # warns that file does not exist
            package = pickle.dumps(False)
            clientSocket.send(package)

        #disabilitando o lock
        lock_control.lock.release()

    print("[port: %s] closed connection with client" % (addr[1]))
    clientSocket.close()