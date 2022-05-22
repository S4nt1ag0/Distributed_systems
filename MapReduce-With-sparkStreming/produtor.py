import socket
import json
import numpy as np
import time
import pickle

lines = open("ratings.dat").read().splitlines()

hostip = '127.0.0.1'
portno = 56789

soc = socket.socket()
soc.bind((hostip, portno))

soc.listen(1)
print("Aguardando comunicação...")
(connection, a) = soc.accept()
print("     OK")
while True:
    print('Enviando linhas')
    lines = np.random.choice(lines,200)
    for line in lines:
        lineJSON = json.dumps(line)
        connection.send(bytes((lineJSON+'\n').encode('utf-8')))
    print("200 linhas enviadas")
    time.sleep(30)