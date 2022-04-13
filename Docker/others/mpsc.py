import asyncio
from datetime import datetime
import tweepy  as tw
import app.utils as utils 


class MyPersonalStreamClient(tw.StreamingClient):
    
    
    def on_tweet(self, tweet):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(utils.run(tweet.data))
        return super().on_tweet(tweet)


    def on_connect(self):
        print("Connection......\n")
        log = {
            "date": str(datetime.now()),
            "type": "On disconnect",
            "msg": "Connection to tweepy.....",
            "status_code": "unavailable"
            }
        utils.write_log(log)
        
        return super().on_connect()


    def on_disconnect(self):
        print("Disconnect tweepy.....\n")
        log = {
            "date": str(datetime.now()),
            "type": "On disconnect",
            "msg": "Disconnect tweepy.....",
            "status_code": "unavailable"
            }
        utils.write_log(log)
        return super().on_disconnect()
    
    def on_errors(self, errors):
        #print("errors")
        #print(errors)
        log = {
            "date": str(datetime.now()),
            "type": "On errors",
            "msg": errors,
            "status_code": "unavailable"
            }
        utils.write_log(log)
        
        return super().on_errors(errors)
    
    def on_closed(self, response):
        print("Closed")
        print(response.status_code == 200)
        
        log = {
            "date": str(datetime.now()),
            "type": "On closed",
            "msg": "Stream connection closed by Twitter",
            "status_code": response.status_code
            }
        utils.write_log(log)
        #print(response.text)
        #self.filter()
        return super().on_closed(response)