import os, json
from functools import lru_cache
import redis


class RedisService(object):

    def __init__(self):
        self.client = redis.Redis(host=os.getenv('REDIS_URL', 'localhost'))

    def add_notifications(self, user_id, data: dict):
        self.client.rpush(f'notifications:{user_id}', json.dumps(data))

    def remove_notifications(self, user_id):
        self.client.delete(f'notifications:{user_id}')

    def get_notifications(self, user_id):
        return self.client.lrange(f'notifications:{user_id}', 0, -1)



@lru_cache()
def get_redis_service():
    return RedisService()


__all__ = ['get_redis_service']