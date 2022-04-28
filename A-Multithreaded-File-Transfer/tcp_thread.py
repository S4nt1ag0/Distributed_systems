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

        # verificando se o arquivo existe no diretorio ou na cache
        if file_control.isExist(directory + res) or res in cache_control.cache:
            # verificando se o tamanho do arquivo não excede o tamanho maximo da cache
            if file_control.getFile_size(directory + res) > cache_control.cache_size:
                print("[port: %s] sending file '%s' to client" % (addr[1], res))
                # preparando o cliente para receber o arquivo
                package = pickle.dumps(True)
                clientSocket.send(package)

                # bloqueando e serializando o arquivo
                with FileLock(directory + res + '.lock'):
                    with open(directory + res, 'rb') as f:
                        package = f.read(BUFFER_SIZE)
                        while package:
                            # enviando os bytes do arquivo
                            clientSocket.send(package)
                            package = f.read(BUFFER_SIZE)
                        sleep(1)
                        f.close()

                print("[port: %s] sent file '%s'" % (
                            addr[1], res))
            else:
                # verificando se o arquivo existe na cache
                if res not in cache_control.cache:

                    print("[port: %s] add file '%s' on cache" % (
                        addr[1], res))
                    size_file = file_control.getFile_size(directory + res)

                    # removendo alguns arquivos na cache para salvar o novo arquivo
                    if cache_control.cache_available < size_file:
                        for key_file in list(cache_control.cache):
                            # remove file from cache
                            if not cache_control.cache[key_file][2]: #verificando se o arquivo não esta com lock
                                print("[port: %s] remove a file '%s' by cache" % (
                                    addr[1], key_file))
                                file_removed = cache_control.cache.pop(key_file)
                                file_removed_size = file_removed[0]
                                cache_control.cache_available += file_removed_size

                    # serializando o arquivo
                    packages = []
                    with open(directory + res, 'rb') as f:
                        package = f.read(BUFFER_SIZE)
                        while package:
                            packages.append(package)
                            package = f.read(BUFFER_SIZE)
                        sleep(1)
                        f.close()

                    # adicionando ele na cache
                    cache_control.cache[res] = [size_file, packages, True]
                    cache_control.cache_available -= size_file

                    print("[port: %s] file '%s' on cache" % (addr[1], res))

                # informando que o arquivo esta bloqueado
                cache_control.cache[res][2] = True

                # salvando informação da cache em variaveis temporarias
                file_in_cache = cache_control.cache[res]
                packages = file_in_cache[1]

                # desbloqueando o arquivo na cache
                cache_control.cache[res][2] = False

                # -------
                # enviando o arquivo através das variaveis temporarias.
                print("[port: %s] sending file '%s' to client through the cache" % (
                    addr[1], res))
                package = pickle.dumps(True)
                clientSocket.send(package)

                for package in packages:
                    clientSocket.send(package)
                sleep(1)
                print("[port: %s] sent file '%s' to client" % (
                    addr[1], res))
        # Se o arquivo não existe
        else:
            print("[port: %s] file '%s' not found" % (addr[1], res))
            # informando que o arquivo não existe
            package = pickle.dumps(False)
            clientSocket.send(package)

        #desabilitando o lock
        lock_control.lock.release()

    print("[port: %s] closed connection with client" % (addr[1]))
    clientSocket.close()