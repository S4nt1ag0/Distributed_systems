import findspark
findspark.init()

import socket
import pickle
from pyspark.sql import SparkSession

BUFFER_SIZE = 1024

spark = SparkSession.builder.getOrCreate()
def load_movie_names(filename):
    movie_names={}
    with open(filename, encoding= 'ISO-8859-1') as f:
        for line in f:
            tokens=line.split('::')
            key=int(tokens[0])
            movie_names[key]=tokens[1]
    return movie_names

movie_names=load_movie_names('movies.dat')

s = socket.socket()
# conectando o socket com o servidor
s.connect(('127.0.0.1', 56797))

data = s.recv(16384)
while data:
    res = pickle.loads(data)
    listReceive = res.split('\n')
    listRDD = spark.sparkContext.parallelize(listReceive)
    movieRatings = listRDD.map(lambda x: (int(x.split('::')[1]), [float(x.split('::')[2]), 1]))
    totalOfMovieRatings = movieRatings.reduceByKey(lambda x, y: [x[0] + y[0], x[1] + y[1]])
    FinalMoviexRating = totalOfMovieRatings.mapValues(lambda x: x[0] / x[1])
    FinalRatingxMovie = FinalMoviexRating.map(lambda kv: (kv[1], kv[0]))
    sortedMovies = FinalRatingxMovie.sortByKey(False)
    results = sortedMovies.take(10)
    for result in results:
        print(movie_names[result[1]], ",", round(result[0], 2))

    data = s.recv(16384)