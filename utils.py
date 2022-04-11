import configparser
import tweepy as tw
import requests


class MyPersonalStreamClient(tw.StreamingClient):

    def on_data(self, raw_data):
        print("on_data")
        print("\n")
        print(raw_data)
        return super().on_data(raw_data)

    
    def on_tweet(self, tweet):# ce qui m'interesse
        print("on_tweet")
        print("\n")
        print(tweet)
        return super().on_tweet(tweet)


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


config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_key = config['twitter']['access_token_key']

bearer_token = config['twitter']['bearer_token']


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r

def initialize_client():
    client = MyPersonalStreamClient(bearer_token = bearer_token,
                                return_type =  requests.Response
                                )
    return client

