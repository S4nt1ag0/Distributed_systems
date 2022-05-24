# A MapReduce Model for movie rating and recommendation
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

***
> Gustavo Santiago Sousa <br>
> Bachelor of Exact and Technological Sciences - UFRB <br>
> Graduating in Computer Engineering - UFRB <br>

- [Getting Started](#Getting_Started)
  - [requisites](#requisites)
  - [Running the application](#Running_the_application) 
- [About The Project](#aboutProject)
  - [Producer](#producer)
  - [Consumer](#Consumer)
    - [MapReduce](#mapReduce) 
- [Final considerations](#finalConsideration)
***
## <a id="Getting_Started" />Getting Started
### <a id="requisites" />Requisites
- [Python 3.6](https://www.python.org/downloads/release/python-360/)
- [numpy](https://numpy.org/)
- [pySpark](https://spark.apache.org/docs/latest/api/python/)
### <a id="Running_the_application" />Running the application

Producer:
```sh
$ python3 producer.py
```

Consumer:
```sh
$ python3 consumer.py
```

 <a id="aboutProject" />About The Project
- 
The system basically consists of two sets of data. One with movie names and their ids, the "movies.dat" and one with the movie id and its rating the "ratings.dat". The idea is that the producer randomly selects 200 lines from the ratings.dat file and sends it to the consumer via socket.

The consumer, in turn, upon receiving the 200 lines, will process the information received by ordering the films in key value pairs by the average of their ratings and display the top 10 films with the highest ratings present in the lines sent by the producer.

*obs: these .dat files are present in this repository

***
## <a id="producer" />Producer

The producer basically reads the "ratings.dat" file separating the ratings by lines.
```sh
lines = open("ratings.dat").read().splitlines()
```
Then it creates a socket and waits for a connection from consumer.py
```sh
hostip = '127.0.0.1'
portno = 56797

soc = socket.socket()
soc.bind((hostip, portno))

soc.listen(1)
print("Aguardando comunicação...")
(connection, a) = soc.accept()
print("     OK")
```
With the connection established, it starts sending data. First it selects 200 random lines with the help of the numpy library, and adds a line break at the end of each line.
serializes the pickle batch and sends the data. Then it waits 30 seconds to start sending another 200 random lines
```sh
while True:
    print('Enviando linhas')
    lines = np.random.choice(lines,200)
    batch = ''
    for line in lines:
        if(batch == ''):batch = line
        else: batch += '\n' + line
    data = pickle.dumps(batch)
    connection.send(data)
    print("200 linhas enviadas")
    time.sleep(30)
```
***

## <a id="consumer" />Consumer

The first thing the consumer does is instantiate a spark section. Then it loads the data from the movie.dat file as a list of key value pairs into memory. The key being the movie id and the value its name
```sh
BUFFER_SIZE = 16384

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
```

With the data loaded, the consumer creates a socket and connects with the producer's socket to start receiving data from movie ratings
```sh
s = socket.socket()
# conectando o socket com o producer
s.connect(('127.0.0.1', 56797))

data = s.recv(BUFFER_SIZE)
while data:
   {...}
    data = s.recv(BUFFER_SIZE)
```
***
### <a id="mapReduce" />MapReduce

With the data from the lines, the task of processing them was divided into five steps

1) Convert the received bytes into a list and then into an RDD list (a list that has the spark map and reduce methods).
```sh
    res = pickle.loads(data)
    listReceive = res.split('\n')
    listRDD = spark.sparkContext.parallelize(listReceive)
```
2) With the RDD list, it's time to create a list of key value pairs, so we created a list of type (movieID: [rating, 1])
```sh
    movieRatings = listRDD.map(lambda x: (int(x.split('::')[1]), [float(x.split('::')[2]), 1]))
```
3) this list was then reduced to pairs that contained the same keys, and their ratings and "1" were summed. This produced value pairs whose value was the total of its ratings and the number of times that movie was rated.
```sh
    totalOfMovieRatings = movieRatings.reduceByKey(lambda x, y: [x[0] + y[0], x[1] + y[1]])
```
4) With the total ratings and how many times the movie was rated, it was easy to determine the average rating of that movie
```sh
    FinalMoviexRating = totalOfMovieRatings.mapValues(lambda x: x[0] / x[1])
```
5) With the new key-value list containing the movieID and its average rating, it became possible to sort the list in descending order according to the average rating

```sh

FinalRatingxMovie = FinalMoviexRating.map(lambda kv: (kv[1], kv[0]))
sortedMovies = FinalRatingxMovie.sortByKey(False)
```

Then the top 10 films were selected and screened, (film name, media rating)

*obs: The movieID was used to access the name in the movie name list
```sh

results = sortedMovies.take(10)
    for result in results:
        print(movie_names[result[1]], ",", round(result[0], 2))
```

***


 <a id="finalConsiderations" />Final considerations
- 
the findSpark library was only needed to find spark for my code due to some difficulties in installing the library.

The buffer_size was initially set to 1Mb and later to 4mb but with this size it was not possible to store all the data sent by the producer (200 lines). So 16mb was adopted, but maybe 8mb values would work