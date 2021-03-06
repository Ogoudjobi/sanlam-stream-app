from concurrent.futures import thread
from datetime import datetime
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional, List, Union
from tweepy import StreamRule
import json
import requests
import utils
from mpsc import MyPersonalStreamClient
import uvicorn



class Rule(BaseModel):
    value : str
    tag : Optional[str] = None


app = FastAPI(debug=True)

@app.on_event("startup")
async def initalization():
    print("Initialization ...")    
    app.state.tw_client = MyPersonalStreamClient(bearer_token = utils.BEARER_TOKEN,
                                return_type =  requests.Response
                                )
    log = {
            "date": str(datetime.now()),
            "type": "On startup",
            "msg": "Startup the app.....",
            "status_code": "unavailable"
            }
    utils.write_log(log)

@app.on_event("shutdown")
async def initalization():
     
    app.state.tw_client.disconnect()
    print("Disconnecting ...")    

    log = {
            "date": str(datetime.now()),
            "type": "On shutdown",
            "msg": "Shutdown the app.....",
            "status_code": "unavailable"
            }
    utils.write_log(log)


@app.get('/')
async def root():
    return {"Message": "MyApp version: {}".format("1.0"),"Info": "Go to /docs"}



@app.get('/manage-rules/retrieve')
async def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=utils.bearer_oauth
    )
    if response.status_code != 200:
        log = {
            "date": str(datetime.now()),
            "type": "Retrieve rules",
            "msg": "Cannot get rules: {}".format(response.text),
            "status_code": response.status_code
            }
        utils.write_log(log)
        
        return {"Message": "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)}
    
    try:
        rules = response.json()["data"]
    except KeyError:
        log = {
            "date": str(datetime.now()),
            "type": "Retrieve rules",
            "msg": "Nothing to retrieve",
            "status_code": "unavailable"
            }
        utils.write_log(log)
        return {"Message": "Nothing to retrieve"}
    
    log = {
        "date": str(datetime.now()),
        "type": "Retrieve rules",
        "msg": response.json(),
        "status_code": response.status_code
        }
    utils.write_log(log)
    return response.json()



@app.get('/tweepy/manage-rules/retrieve')
async def get_rules_tweepy():
    response = app.state.tw_client.get_rules()
    if response.status_code != 200:
        return  {"Message" : "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text) }
    
    try:
        rules = response.json()["data"]
    except KeyError:
        return {"Message": "Nothing to retrieve"}
    
    return {"Message":{
        "data": response.json()["data"],
        "total": response.json()["meta"]["result_count"],
        "remaining": 5-int(response.json()["meta"]["result_count"])
        }}



@app.post('/manage_rules/create')
async def add_rules(rules : List[Rule]):
    rules_json = jsonable_encoder(rules)
    payload = {"add": rules_json}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=utils.bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        return {"Message": "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)}
    
    print(response.json())
    return {"Message" : "Rule add successfully" if len(rules) == 1 else "{} rules add successfully".format(len(rules))}



@app.post('/tweepy/manage_rules/create')
async def add_rules_tweepy(rules : List[Rule]):
    rules_json = jsonable_encoder(rules)
    stream_rules = [StreamRule(**rule) for rule in rules_json]
    response = app.state.tw_client.add_rules(add=stream_rules)

    if response.status_code != 201:
        return  {"Message" : "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text) }
 
    return {
        "Message" : "Rule add successfully" if len(rules) == 1 else "{} rules add successfully".format(len(rules)),
        "Not_created": response.json()["meta"]["summary"]["not_created"],
        "Invalid": response.json()["meta"]["summary"]["invalid"]
        }



@app.post('/manage_rules/clean-all')
async def delete_all_rules():
    
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=utils.bearer_oauth
    )
    
    try:
        rules = response.json()["data"]
    except KeyError:
        return {"Message": "Nothing to remove"}
    
    ids = list(map(lambda rule: rule["id"], rules))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=utils.bearer_oauth,
        json=payload
    )
    
    if response.status_code != 200:
        return {"Message": "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text )}
    return {"Message" : response.json()}



@app.post('/tweepy/manage_rules/clean-all')
async def delete_all_rules_tweepy():
     
    response =  app.state.tw_client.get_rules()
    
    try:
        rules = response.json()["data"]
    except KeyError:
        return {"Message": "Nothing to remove"}
    
    ids = list(map(lambda rule: rule["id"], rules))  
      
    response = app.state.tw_client.delete_rules(ids=ids)

    if response.status_code != 200:
        return {"Message": "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text)}

    return {"Message":response.json()}



@app.post('/manage_rules/clean-somes')
async def delete_some_rules(indices : Union[List[int], int]):
    
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=utils.bearer_oauth
    )
    
    try:
        rules = response.json()["data"]
    except KeyError:
        return {"Message": "Nothing to remove"}
    
    ids = list(rules[indices]["id"]) if isinstance(ids, int) else [rules[id]["id"] for id in indices] 
    
    payload = {"delete": {"ids": ids}}
    
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=utils.bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        return {"Message": "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text)}
    return {"Message" : response.json()["summary"]}



@app.post('/tweepy/manage_rules/clean-somes')
async def delete_some_rules_tweepy(indices : Union[List[int], int]):
    
    response =  app.state.tw_client.get_rules()
    
    try:
        rules = response.json()["data"]
    except KeyError:
        return {"Message": "Nothing to remove"}
    
    ids = rules[indices]["id"] if isinstance(ids, int) else [rules[id]["id"] for id in indices] 
    response = app.state.tw_client.delete_rules(ids)  
    
    
    if response.status_code != 200:
        return {"Message": "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text)}

    return {"Message" : response.json()["summary"]}


@app.get('/stream/get-stream')
async def get_stream():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=utils.bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            print(json.dumps(json_response, indent=4, sort_keys=True))


@app.get('/tweepy/stream/get-stream')
async def get_stream_tweepy():
    try:
        app.state.tw_client.get_rules().json()["data"]
    except KeyError:
        return {"Message": "No rule(s) to filter" }
    try:
        thread = app.state.tw_client.filter(threaded = True)
    except:
        stop_stream_tweepy()
        return {"Message": "An error occurred" }



@app.get('/tweepy/stream/stop-stream')
async def stop_stream_tweepy():
    app.state.tw_client.disconnect()
    return{"Message" : "Stream Stopped"}
