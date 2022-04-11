import tweepy 
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_key = config['twitter']['access_token_key']

bearer_token = config['twitter']['bearer_token']
#authentication

client = tweepy.StreamingClient(bearer_token=bearer_token)

query = 'from:suhemparack -is:retweet'

"""
tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'], max_results = 100)

for tweet in tweets.data:
    print(tweet.text)
    if len(tweet.context_annotations) > 0:
        print(tweet.context_annotations)

auth = tweepy.OAuthHandler(
    api_key, 
    api_key_secret
)

auth.set_access_token(
    access_token,
    access_token_key
)

api = tweepy.API(auth)

public_tweets = api.home_timeline()

print(public_tweets)
client = tweepy.StreamingClient(bearer_token=bearer_token)

print(client.get_rules())

print(tweepy.__version__)
print(client.running)
client.delete_rules(["1510604318763855873", "1510605841879257107"])
client.disconnect()"""


"""query = 'sanlam assurance'

tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'], max_results=100)

for tweet in tweets.data:
    print(tweet.text)
    if len(tweet.context_annotations) > 0:
        print(tweet.context_annotations)"""
        
client.delete_rules(ids=["1510750509224890380","1510755461733179405", "1512485233609871363", "1512485680546516998"])

client.disconnect()
        
print(tweepy.__version__)