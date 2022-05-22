import findspark
findspark.init()

import time
import json
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark import StorageLevel

socket = SparkContext(appName="Demo")
streamingSocket = StreamingContext(socket, 30)


socketStreaming = streamingSocket.socketTextStream("127.0.0.1",56789)

linesJSON = socketStreaming.map(lambda line: json.loads(line))
linesJSON.pprint()

movieRatings = linesJSON.map(lambda x: (int(x.split('::')[1]), [float(x.split('::')[2]),1]))

totalOfMovieRatings = movieRatings.reduceByKey(lambda x, y: [x[0] + y[0],x[1]+y[1]])
linesJSON.map(lambda line: np.fromstring(line,np.int8))

print(lines)
lines.pprint()

streamingSocket.start()

streamingSocket.awaitTermination()