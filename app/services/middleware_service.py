import redis
from rate_limit_class import TokenBucket

# Create a Redis connection
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Create a rate limiter: 10 requests per second
limiter = TokenBucket(
    redis_client=r,
    capacity=2,        # Maximum burst size
    refill_rate=1,      # Add 1 token per interval
    refill_interval=20.0 # Every 1 second
)
