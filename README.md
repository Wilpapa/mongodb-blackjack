# MongoDB Blackjack

Blackjack games simulator with data storage in MongoDB for game analysis.

# How to start

## MongoDB

You will need to start a MongoDB instance to store the game results.

### Start MongoDB locally

If you want to work locally, you can install and run MongoDB yourself or you can use Docker.

```
docker run --rm -d -p 27017:27017 --name mongodb mongo:4.0.7
```

If you use this Docker command line or a MongoDB instance running locally, you will need to use the following URI to use your MongoDB instance.

```
mongodb://localhost
```

### Use MongoDB in the Cloud with MongoDB Atlas

You can also create a free MongoDB cluster with [MongoDB Atlas](https://cloud.mongodb.com).

If you want to connect to this instance, you will need to:

- Create a free account on MongoDB Atlas.
- Start a free tier cluster.
- In the security tab at the top create a MongoDB user with read/write permissions at least.
- In the IP whitelist in the security tab, add your current public IP address to the list of authorised IP address.

Once this is done, you will be able to connect to this MongoDB cluster in the cloud from your computer using the provided URI when you click on the *connect* button.

This should look like this one:

```
mongodb+srv://<username>:<password>@freesandbox-rirxn.mongodb.net/test?retryWrites=true
```

# Start the python program

You have to use python 3 and you have to install the dependencies.

```
sudo pip3 install -r requirements.txt
```

Then you just have to execute the program with the correct MongoDB URI.

For example:

```
python mongo-blackjack.py mongodb://localhost
```

Finally, you will find the documents in MongoDB:

```js
> use blackjack
switched to db blackjack
> db.games.findOne()
{
	"_id" : ObjectId("5c9a777597a19056bd168971"),
	"TS" : ISODate("2019-03-26T20:03:17.013Z"),
	"sample" : 0,
	"threshold" : 15,
	"playerHand" : [
		3,
		1,
		6
	],
	"casinoHand" : [
		8,
		4,
		6
	],
	"playerBlackjack" : false,
	"casinoBlackjack" : false,
	"playerScore" : 20,
	"casinoScore" : 18,
	"playerGain" : 1
}
```

## Contributors

- Samuel Meister : for the original idea and designing the global algorithm
- Tatiana Meister : for support when rewriting code in OOP
- Maxime Beugnet : for the code review and this awesome README :-).
