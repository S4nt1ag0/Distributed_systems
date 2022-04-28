# A Multithreaded File Transfer with Cache and Locking
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

***
> Gustavo Santiago Sousa <br>
> Bachelor of Exact and Technological Sciences - UFRB <br>
> Graduating in Computer Engineering - UFRB <br>

- [Getting Started](#Getting_Started)
  - [requisites](#requisites)
  - [Running the application](#Running_the_application) 
- [About The Project](#aboutProject)
  - [Client](#client)
  - [Server](#server)
    - [Thread](#thread)
    - [Cache](#cache)
    - [lock](#lock)
***
## <a id="Getting_Started" />Getting Started
### <a id="requisites" />Requisites
- [Python 3.6](https://www.python.org/downloads/release/python-360/)
- [filelock](https://pypi.org/project/filelock/)
### <a id="Running_the_application" />Running the application

Server:
```sh
python tcp_server.py localhost 9098 ./files/
```

Client:
```sh
python tcp_client.py localhost 9098 image.jpg .
or
python tcp_client.py localhost 9098 list
```

<video width="320" height="240" controls>
  <source src="./assets/demostration.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>

 <a id="aboutProject" />About The Project
- 
The System basically consists of a server that receives as a parameter the port on which it will run and a directory to which it must fetch the files. And a client that connects to that server informing the server address and port. Once connected, the client can perform a search for files informing the name of the file and a directory that wants to save the file returned from the server. It is also possible for the client to request a list of the files stored in the cache memory, instead of requesting a file. For the latter case it is enough to pass the reserved word "list" as a parameter instead the file name and the directory to save.

*obs: a folder with some files are in this repo for usage like example

- Checks the existence of the file in the directory from which the server is directed;
- Checks whether the file is present in the cache memory;
     - If the file is not in the cache, the server will try to allocate that file:
         - The available space for allocating a new file will be checked;
         - Files will be removed from memory to free up space, when necessary;
         - The file will be serialized in packets, according to the size of the transition buffer;
     - If the file is present, it is sent to the applicant;
     - If the file is larger than the maximum cache limit (64MB), it is not allocated to memory;
- Send the file when available;

***
## <a id="client" />Client

The Client after creating the socket and connecting to the server can work in two different ways:
1) When the client receives 5 parameters in the input, ex:
```sh
python localhost 9098 image.jpg ./receives
```
it understands that it will perform a file search. and after sending the 4th parameter to the server, it waits for a file back that will be saved at the given address.
```sh
# caminho para salvar o arquivo
    path_to_save = save_directory + res
    # criando buffer para armazenar a resposta do servidor
    buffer = s.recv(BUFFER_SIZE)
    # carregando buffer com os dados enviados do servidor
    res = pickle.loads(buffer)
    if res:
        with open(path_to_save, 'wb') as file:
            print('downloading', res)
            package = s.recv(BUFFER_SIZE)
            while package:
                file.write(package) # salvando o arquivo no disco
                package = s.recv(BUFFER_SIZE)
            file.close()
        print("file '%s' saved!" % (res))
    else:
        print("file '%s' not found" % (res))
```
2) When the client receives 4 parameters at the input, ex:
```sh
python localhost 9098 list
```
it understands that it will query the files available in the cache and only displays the list returned by the server
```sh
    data = s.recv(BUFFER_SIZE)
    while data:
        res = pickle.loads(data)
        print(res)
        data = s.recv(BUFFER_SIZE)
```
***

## <a id="server" />Server

The server initializes a TCP socket with the port informed by the user and starts a process to listen for new connections from the client. When the server receives a connection request from the client, a new instance of the connection is generated and assigned to a new Thread, passing the connection, the client's address and the address to which the server must search.
```sh
try:
    while True:
        # aceitando conexão com o client
        clientSocket, addr = s.accept()
        print('[port: %s] new connection with client' % (addr[1]))

        # a new thread client
        start_new_thread(threaded, (clientSocket, addr, directory))
except:
    pass
finally:
    print("SERVER OFF %s:%s" % (HOST, PORT))
    # fechando a conexão do servidor quando o server encerra
    s.close()
```
***
### <a id="thread" />Thread

On the thread all the main processing of the request is done. It is the core of the server and consists of the following decision flow

- Get the message sent by the server and deserialize
- if the message is equals as "list" :
  - get the keys from the tuples present in the cache and return to the client a list of these keys
- else:
  - check if the message sent by the user is a tuple key present in the cache or if there is a file with the same name as the message inside the server's search directory
    - If the file does not exist in the cache and its size is greater than the total size of the cache, only the file present in the directory is serialized and sent.
    - If the file does not exist in the cache but its size allows it to be stored in the cache, it is inserted into it.
      - If there is space it will be placed in the cache and the lock for this file activated.
      - If there is no space, the unblocked files from the cache will be deleted until the cache has enough space to store this new file.
    - The cache file is saved in a temporary variable, the block is released, the file is sent to the client and the connection is closed.
  - else : return not found file and close conection

***
### <a id="cache" />Cache

the cache file defines the variables: cache, available size and cache size globally. Then the server imports this file to define the initial values of these variables. And the Thread imports these variables to manipulate (query and save) the cache and consequently the size available in it.

The cache consists of a Map where the name of the file is its key and the value is an array with the size of the file, the vector of bytes representing the serialized file and a boolean to indicate if that file is locked or not (lock)

this way (<file_name>,[ file_size, file_in_bytes[], lock ])
***
### <a id="Lock" />Lock

To lock the files, the python filelock library was used, which locks the file as the thread performs the serialization of the file on disk or when it performs the serialization to cache.

