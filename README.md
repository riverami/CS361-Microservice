# CS361-Microservice

REQUEST:
Data can be requested from the microservice by using Python Socket and connecting to the same host and port on your client program.
Ex. host = socket.gethostname() port = 5000

Then on your program you will send a message to the microservice similar to a function call.

So to get all rows in a movie database that are about a movie called "Test Movie" you would send the message "GET, 'Test Movie'". The first word in the message is a keyword to tell the microservice which type of function to use.

Similarly, to insert data to the same database you would use the POST keyword as follows. "POST, 'Movie Title', 1971, 6.7". The first word is a keyword and the remaining values are for the columns in the database. In the prior example it was the movie title, year released, and average score.

RECEIVE:
After sending the message to the microservice, the service will return a string either with the returned database data, a confirmation message of data being entered, or a message to check the data you're putting in. This information can then be manipulated in your program as needed.

![21](https://user-images.githubusercontent.com/71803404/199147555-8dcf3ccd-a9df-437e-92fe-b188be9f489a.PNG)
