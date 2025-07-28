import json
from common_api.services.v0 import get_redis_api_db, Logger

logger = Logger()

class CacheService:
    def __init__(self):
        self.redis = get_redis_api_db()
    
    def get_database_credential(self, licence_uuid):
        try:
            cache_key = f"{licence_uuid}_database"
            credential = self.redis.get(cache_key)
            if not credential:
                raise ValueError(f"No database credential found for licence {licence_uuid}")
                
            json_string = credential.replace("'", "\"")
            return json.loads(json_string)
        except Exception as e:
            logger.error(f"Error retrieving database credential: {e}")
            raise ValueError(f"Failed to retrieve database credential: {e}")
    
    def store_context(self, secret, payload, ttl):
        try:
            cache_key = f"context_{secret}"
            self.redis.set(cache_key, json.dumps(payload), ex=ttl)
            logger.info(f"Stored context for secret {secret}")
        except Exception as e:
            logger.error(f"Error storing context: {e}")
            raise ValueError(f"Failed to store context: {e}")
    
    def get_context(self, secret):
        try:
            cache_key = f"context_{secret}"
            context = self.redis.get(cache_key)
            if not context:
                raise ValueError(f"No context found for secret {secret}")
                
            return json.loads(context)
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            raise ValueError(f"Failed to retrieve context: {e}")