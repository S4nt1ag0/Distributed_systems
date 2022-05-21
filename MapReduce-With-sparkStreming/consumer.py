import findspark
findspark.init()

import time
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark import StorageLevel

socket = SparkContext(appName="Demo")
streamingSocket = StreamingContext(socket, 30)


socketStreaming = streamingSocket.socketTextStream("127.0.0.1",56789)
lines = socketStreaming.flatMap(lambda line: line.split("\n"))
print('----------')
print(lines)
print('----------')

def convertToJSON(entry):
    return json.loads(entry)


def splitEntry(entry):
    data = list()
    for reg in entry:
        data.append((reg[1], reg[2]))
    return data


dataJson = socketStreaming.map(convertToJSON)


pairs = dataJson.map(splitEntry)

print(pairs)
print('<<<')
pairs.pprint()
