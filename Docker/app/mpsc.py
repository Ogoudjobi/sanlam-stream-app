import tweepy  as tw

class MyPersonalStreamClient(tw.StreamingClient):
    
    def on_tweet(self, tweet):# ce qui m'interesse
        return tweet


    def on_connect(self):
        print("Connection...\n")
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