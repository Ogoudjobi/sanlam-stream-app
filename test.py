import asyncio
import aioredis

def decode_dict(truc: dict):
    new =  dict()
    for k,v in truc.items():
        new[k.decode("utf-8")] = v.decode("utf-8")
    return new

async def get_redis_pool() -> aioredis.Redis:
    redis = await aioredis.from_url(
        "redis://localhost", encoding="utf-8", decode_responses=True
    )
    return redis

async def main():
    redis = await get_redis_pool()
    await redis.set("hash1", "value2")
    
    r = await redis.incr("cpt",10)
    print(r)
    result = await redis.hgetall("hash")
    #await redis.incr("cpt")
    #result2 = await redis.getkeys()
    print(result)
    print("\n")
    #print(result2)
    #print(decode_dict(result))
    await redis.close()


if __name__ == "__main__":
    asyncio.run(main())


