import findspark
findspark.init()

import time
import pickle
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark import StorageLevel

socket = SparkContext(appName="Demo")
streamingSocket = StreamingContext(socket, 30)


socketStreaming = streamingSocket.socketTextStream("127.0.0.1",56789)
lines = socketStreaming.flatMap(lambda line: pickle.loads(line))

print(lines)
lines.pprint()

lines.map(lambda line: np.fromstring(line,np.int8))

print(lines)
lines.pprint()

# movieRatings = interactions.map(lambda x: (int(x.split('::')[1]), [float(x.split('::')[2]),1]))
#     totalOfMovieRatings = movieRatings.reduceByKey(lambda x, y: [x[0] + y[0],x[1]+y[1]])

# res = pairs.reduceByKey(lambda a, b: a+b)

# res.pprint()

# ratings = ssc.textFileStream("../database/").map
# ratings.pprint()

streamingSocket.start()

streamingSocket.awaitTermination()
# WARN RandomBlockReplicationPolicy: Expecting 1 replicas with only 0 peer/s.
# WARN BlockManager: Block input-0-1653087338600 replicated to only 0 peer(s) instead of 1 peers