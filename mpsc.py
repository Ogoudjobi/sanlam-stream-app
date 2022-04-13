import asyncio
import tweepy  as tw
import utils 
#import nest_asyncio


#nest_asyncio.apply()

class MyPersonalStreamClient(tw.StreamingClient):
    
    def on_tweet(self, tweet):# ce qui m'interesse
        #print(tweet.data)
        #asyncio.create_task(utils.run(tweet.data))
        #asyncio.ensure_future(utils.run(tweet.data))
        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(utils.run(tweet.data))
        
        
        
        return super().on_tweet(tweet)


    def on_connect(self):
        print("Connection......\n")
        return super().on_connect()


    def on_disconnect(self):
        print("Disconnect tweepy.....\n")
        
        return super().on_disconnect()
    
    def on_errors(self, errors):
        print("errors")
        print(errors)
        return super().on_errors(errors)
    
    def return_stream_tweet(self):
        ...