import redis.asyncio as redis
from fastapi_redis_cache import FastApiRedisCache, cache

from src.config import (REDIS_DATABASE, REDIS_HOST, REDIS_PORT)


redis_client = None

async def init_redis_pool():
    global redis_client
    redis_client = redis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DATABASE}")
    return redis_client

def init_redis_cache(app):
    FastApiRedisCache().init(
        host_url=f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DATABASE}",
        prefix="fastapi-cache",
        
        # expire=3600,
        # app=app
    )