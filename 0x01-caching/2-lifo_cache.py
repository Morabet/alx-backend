#!/usr/bin/env python3
""" LIFO Caching"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ Defining LIFO Caching"""

    def __init__(self):
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache"""
        if key in self.cache_data and item:
            del self.cache_data[key]
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            last_key = self.cache_data.popitem()
            print(f"DISCARD: {last_key[0]}")
        self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key """
        if key and key in self.cache_data:
            return self.cache_data[key]
        return None
