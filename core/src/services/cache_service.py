from redis import Redis
from typing import Any, Optional

class CacheService:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        """Set a value in the cache with an optional expiration time."""
        self.redis_client.set(key, value, ex=expire)

    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache."""
        return self.redis_client.get(key)

    def delete(self, key: str) -> None:
        """Delete a value from the cache."""
        self.redis_client.delete(key)

    def exists(self, key: str) -> bool:
        """Check if a key exists in the cache."""
        return self.redis_client.exists(key) > 0