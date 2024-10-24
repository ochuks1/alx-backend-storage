#!/usr/bin/env python3
"""
This module contains the Cache class for interacting with Redis,
decorators for counting method calls and tracking call history,
and a replay function to display call history.
"""

import redis
import uuid
import functools
from typing import Union, Callable


class Cache:
    """ Cache class for interacting with Redis data store. """

    def __init__(self):
        """
        Initialize Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @functools.wraps
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generate a random key and store the given data in Redis.

        Args:
            data (Union[str, bytes, int, float]): The data to store in Redis.

        Returns:
            str: The key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis and apply a transformation function if provided.

        Args:
            key (str): The Redis key to retrieve the data from.
            fn (Callable, optional): A function to transform the data. Defaults to None.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data, possibly transformed.
        """
        data = self._redis.get(key)
        if data is not None and fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieve string data from Redis.

        Args:
            key (str): The Redis key to retrieve the data from.

        Returns:
            str: The data as a string.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieve integer data from Redis.

        Args:
            key (str): The Redis key to retrieve the data from.

        Returns:
            int: The data as an integer.
        """
        return self.get(key, int)


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called using Redis.

    Args:
        method (Callable): The method to wrap.

    Returns:
        Callable: The wrapped method with counting functionality.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to increment the call count and call the original method.

        Args:
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method.

        Returns:
            The result of the original method.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a method in Redis.

    Args:
        method (Callable): The method to wrap.

    Returns:
        Callable: The wrapped method with history tracking.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper to log inputs and outputs for the decorated method.

        Args:
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method.

        Returns:
            The result of the original method.
        """
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))

        return output
    return wrapper


@call_history
@count_calls
def store(self, data: Union[str, bytes, int, float]) -> str:
    """
    Store data, count calls, and log method call history.

    Args:
        data (Union[str, bytes, int, float]): The data to store.

    Returns:
        str: The key under which the data is stored.
    """
    key = str(uuid.uuid4())
    self._redis.set(key, data)
    return key


def replay(method: Callable):
    """
    Display the history of calls to the given method using Redis.

    Args:
        method (Callable): The method to display call history for.
    """
    r = redis.Redis()
    method_name = method.__qualname__
    input_key = method_name + ":inputs"
    output_key = method_name + ":outputs"

    input_list = r.lrange(input_key, 0, -1)
    output_list = r.lrange(output_key, 0, -1)

    print(f"{method_name} was called {len(input_list)} times:")

    for inp, out in zip(input_list, output_list):
        print(f"{method_name}(*{inp.decode('utf-8')}) -> {out.decode('utf-8')}")
