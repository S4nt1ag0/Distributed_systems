import socket
import sys
import pickle

BUFFER_SIZE = 1024

# criando socket
s = socket.socket()

host = sys.argv[1]            # host
port = int(sys.argv[2])       # port
res = sys.argv[3]             # file_name
save_directory = sys.argv[4]  # path to save file
if save_directory[len(save_directory) - 1] != '/': save_directory += '/' #add / ao final do diretorio de salvamento
if save_directory == '.' or save_directory == './' : save_directory = ''

# conectando o socket com o servidor
s.connect((host, port))

# transformando a mensagem em uma cadeia de bytes
msg = pickle.dumps((res))

# enviando dados
s.sendall(msg)

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