import aioredis
import configparser
from typing import Optional, List, Union, Dict


config = configparser.ConfigParser()
config.read('config.ini')

HOST = config['redis']['HOST']
ENCODING = config['redis']['ENCODING']


class MyRedisCon:


    def __init__(self,host: str = "localhost", encoding: str = "utf-8", decode_reponse : bool= True ) -> None:
        self._host = host
        self._encoding = encoding
        self._decode_reponse = decode_reponse
        try:
            self._redis =  aioredis.from_url(
                "redis://"+host, 
                encoding= encoding
            )
        except:
            self._redis =  None
        


    async def create_pool(self)-> Union[aioredis.Redis, None]:
        try:
            redis =  await aioredis.from_url(
                "redis://"+self._host, 
                encoding= self._encoding
                
            )
        except:
            print("Enable to create connection")
            return None

        return redis

    async def write_data(self, key: str, value: Union[Dict[str,Union[str,int,float]], str]) -> dict: 
        if self._redis == None:
            self._redis = await self.create_pool()
        
        if isinstance(value,str):
            await self._redis.set(key, value)
            return {"Message": "Done successfully"}
        
        await self._redis.hset(key, mapping = value)
        return {"Message": "Done successfully"}
            

    
    async def get_data(self,key:str, flag:str)-> Union[str,dict]:
        if self._redis == None:
            self._redis = await self.create_pool()
            
        if flag == "set":
            result = await self._redis.get(key)
            return result
        if flag == "hset":
            result =  await self._redis.hgetall(key)
            return result
        
        
    async def del_data(self,key:Union[str,List[str]], flag:str)-> Union[str,dict]:
        if self._redis == None:
            self._redis = self.create_pool()
            if isinstance(str,key):
               result = await self._redis.delete(key)
            else:
                result = await self._redis.delete(*key)
            
            return result
        
    async def disconnect(self):
        if self._redis == None:
            return {"Message": "Nothing to close"}
        await self._redis.close()
        return {"Message": "Connection sucessfully closed"}