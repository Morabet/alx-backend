#!/usr/bin/env python3
""" FIFO caching"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ Defining FIFO caching"""

    def __init__(self):
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache"""
        if key and item:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                first_key = list(self.cache_data.keys())[0]
                del self.cache_data[first_key]
                print(f"DISCARD: {first_key}")

            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key """
        if key and key in self.cache_data:
            return self.cache_data[key]
        return None
