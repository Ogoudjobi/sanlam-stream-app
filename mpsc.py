import tweepy  as tw
import utils 

class MyPersonalStreamClient(tw.StreamingClient):
    i = 0
    def on_tweet(self, tweet):# ce qui m'interesse
        #utils.run(tweet)
        i+=1
        return super().on_tweet(tweet)


    def on_connect(self):
        print("Connection......\n")
        return super().on_connect()


    def on_disconnect(self):
        print("Good-Bye!!\n")
        
        return super().on_disconnect()
    
    def on_errors(self, errors):
        print("errors")
        print(errors)
        return super().on_errors(errors)
    
    def return_stream_tweet(self):
        ...