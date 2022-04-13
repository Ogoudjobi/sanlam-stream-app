from datetime import datetime
from app.credentials import BEARER_TOKEN,CONNECTION_STRING, EVENT_HUB_NAME
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import json
import os

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


async def run(data):
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    print(data)
    producer = EventHubProducerClient.from_connection_string(conn_str=CONNECTION_STRING, eventhub_name=EVENT_HUB_NAME)
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        event_data_batch.add(EventData(json.dumps(data)))

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)
    
    
def write_log(log):
    base_dir = "./Log/"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        
    file_name = "Log-"+str(datetime.now().date())+".log"
    if not os.path.isfile(base_dir+file_name):
        with open(base_dir+file_name,'w') as f:
            json.dump(log,f,indent=4,separators=(',',': '))
            
    else:
        with open(base_dir+file_name,'a') as f:
            json.dump(log,f,indent=4,separators=(',',': '))

