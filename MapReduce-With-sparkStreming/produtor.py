import socket
import json
import numpy as np
import time

lines = open("ratings.dat").read().splitlines()

def lines_generator():
    while True:
        myline = np.random.choice(lines,200)
        yield json.dumps(myline)
        time.sleep(30)

hostip = '127.0.0.1'
portno = 56789 

#listener need to be started before!
#try: netcat -lkp 56789
#before you start with spark streaming

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
soc.connect((hostip, portno))

it = line_generator()
for l in it:
    soc.send(l.encode('utf8'))