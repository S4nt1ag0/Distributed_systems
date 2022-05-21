import socket
import json
import numpy as np
import time
import pickle

lines = open("ratings.dat").read().splitlines()

hostip = '127.0.0.1'
portno = 56789

#listener need to be started before!
#try: netcat -lkp 56789
#before you start with spark streaming

soc = socket.socket()


print('antes connect')
soc.bind((hostip, portno))

print('------')

soc.listen(1)

(connection, a) = soc.accept()
print('passou connection')

while True:
    print('Enviando linhas')
    myline = np.random.choice(lines,200)
    #print(myline)
    #serialized_data = pickle.dumps(myline, protocol=2)
    myline2 = np.array2string(myline)
    serialized_data = pickle.dumps((myline2))
    connection.send(serialized_data)
    time.sleep(30)