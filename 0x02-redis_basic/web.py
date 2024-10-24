#!/usr/bin/env python3
"""
Web cache and tracker module
"""

import redis
import requests
from typing import Callable

r = redis.Redis()


def count_access(fn: Callable) -> Callable:
    """
    Decorator to count how many times a URL is accessed.
    """
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        r.incr(count_key)  # Increment access count
        return fn(url)
    return wrapper


@count_access
def get_page(url: str) -> str:
    """
    Retrieves the content of a URL and caches it with an expiration.
    """
    cache_key = f"cached:{url}"
    cached_content = r.get(cache_key)

    if cached_content:
        return cached_content.decode('utf-8')

    response = requests.get(url)
    r.setex(cache_key, 10, response.text)  # Cache for 10 seconds

    return response.text
