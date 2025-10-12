import redis

from app.config.config import settings


redis_connection = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

# Redis lock
redis_lock = redis_connection.lock("Redis-Lock", timeout=5)