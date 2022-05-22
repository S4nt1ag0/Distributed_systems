import findspark
findspark.init()

import time
import json
from pyspark import SparkContext
from pyspark.conf import SparkConf
from pyspark.streaming import StreamingContext
from pyspark import StorageLevel

conf = SparkConf()
conf.setAppName('Demo').set("spark.executor.memory", "500M").set("spark.driver.memory", "500M")


socket = SparkContext(conf=conf)
streamingSocket = StreamingContext(socket,45)


socketStreaming = streamingSocket.socketTextStream("127.0.0.1",56789)

linesJSON = socketStreaming.map(lambda line: json.loads(line))
linesJSON.pprint()

movieRatings = linesJSON.map(lambda x: (int(x.split('::')[1]), [float(x.split('::')[2]),1]))

print(movieRatings)

streamingSocket.start()

streamingSocket.awaitTermination()