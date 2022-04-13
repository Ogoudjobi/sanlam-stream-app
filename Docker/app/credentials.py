import configparser

config = configparser.ConfigParser()
config.read('app/config.ini')

API_KEY = config['twitter']['API_KEY']
API_KEY_SECRET = config['twitter']['API_KEY_SECRET']

ACCESS_TOKEN = config['twitter']['ACCESS_TOKEN']
ACCESS_TOKEN_KEY = config['twitter']['ACCESS_TOKEN_KEY']

BEARER_TOKEN = config['twitter']['BEARER_TOKEN']

EVENT_HUB_NAMESPACE = config['azure-event-hub']['EVENT_HUB_NAMESPACE']
EVENT_HUB_NAME = config['azure-event-hub']['EVENT_HUB_NAME']
CONNECTION_STRING = config['azure-event-hub']['CONNECTION_STRING']


CONNECTION_STRING_STORAGE = config['azure-storage-account']['CONNECTION_STRING_STORAGE']
STORAGE_ACCOUNT_NAME = config['azure-storage-account']['STORAGE_ACCOUNT_NAME']
BLOB_CONTAINER = config['azure-storage-account']['BLOB_CONTAINER']