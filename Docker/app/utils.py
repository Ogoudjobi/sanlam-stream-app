import configparser
import requests
from app.mpsc import *

config = configparser.ConfigParser()
config.read('app/config.ini')

API_KEY = config['twitter']['api_key']
API_KEY_SECRET = config['twitter']['api_key_secret']

ACCESS_TOKEN = config['twitter']['access_token']
ACCESS_TOKEN_KEY = config['twitter']['access_token_key']

BEARER_TOKEN = config['twitter']['bearer_token']


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


