# MongoDB Blackjack

Blackjack games simulator with data storage in MongoDB for game analysis.

"Dad, do you think there's a simple way to win against the dealer in Casino Blackjack ? what if we stand at 15 - for example ?"

The whole story about this piece of code is taking advantage of my son curiosity for the maths behind Blackjack casino game to lead him into algorithm design, object programming, writing clean documented code and, of course, having fun with MongoDB (do you know a **cooler** database engine ?!).

Basic principle is as follow :
* Player will draw cards until score reaches THRESHOLD value or gets busted
* Then if player did not cross 21, Casino will draw cards until score reaches 17 or gets busted

As all games are recorded into MongoDB database, it's easy to run some aggregation pipelines to gather statistics, see last chapter of this README.

The program is counting player gains as follow :
* Player does a blackjack and Casino does not : 2 
* Player and Casino get a blackjack : 0
* Player busted or Casino has a blackjack while player has not : -1
* Player wins on Casino : 1

The program can be improved in several ways :
- implement Double and Split
- take Casino cards into account for hitting cards decision making
- adapt hitting strategy depending on number of cards in hand

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

### You have to use python 3 and you have to install the dependencies.

```
sudo pip3 install -r requirements.txt
```

### Edit mongo-blackjack.py and set the values you want to use :

```
MONGO_URI = "mongodb://localhost" # URI to connect to MongoDB
SAMPLES = 1000  # number of games to play
THRESHOLD = 15  # score under which Player will draw 1 card
NB_DECKS = 4  # number of decks to use. Decks are reshuffled when half the cards have been drawn
```

### Then you just have to execute the program

For example:

```
python3 mongo-blackjack.py
```

# Analyze games

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

### Example of analytic queries

You can filter a game session on TS field (contains the datetime when you launched the test)

Create an index on TS (will make the queries run *a lot* faster)
```js
db.games.createIndex({TS:1})
```

Find the latest run
```js
db.games.find({},{_id:0,TS:1}).sort({TS:-1}).limit(1)
```

List all runs with timestamp, threshold, #games, total gains/losses
```js
db.games.aggregate([
	{$group:{
		_id:"$TS",
		games:{$sum:1}, 
		threshold:{$max:"$threshold"},
		gains:{$sum:"$playerGain"}
		}
	},
	{$sort:{_id:-1}}
])
```

Evaluate total gain for a run
```js
db.games.aggregate([
	{$match:{"TS" : ISODate("2019-03-26T12:10:51.456Z")}},
	{$group:{_id:"Gain total",total:{$sum:"$playerGain"}}}
])
```

Compute blow lost ratio (games lost due to total score over 21)
```js
condition={
	"$cond" : {
		"if" : {
			"$gte" : [
				"$playerScore",
				22
			]
		},
		"then" : 1,
		"else" : 0
	}
}

db.games.aggregate([
	{$match:{"TS" : ISODate("2019-03-26T12:10:51.456Z")}},
	{$project:{blow:condition}},
	{$group:{_id:"counts",blows:{$sum:"$blow"},total:{$sum:1}}},
	{$project:{"blow ratio":{$divide:["$blows","$total"]}}}])
```

# Contributors

- Samuel Meister : for the original idea and designing the global algorithm
- Tatiana Meister : for support when rewriting code in OOP
- Maxime Beugnet : for the code review and starting this awesome README :-).
