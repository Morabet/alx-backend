#!/usr/bin/env python3
"""  MRU Caching"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ Defining  MRU Caching"""

    def __init__(self):
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """ Add an item in the cache"""
        if key and item:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                last_key = self.queue.pop()
                if key not in self.cache_data:
                    del self.cache_data[last_key]
                    print(f"DISCARD: {last_key}")

            self.cache_data[key] = item
            self.queue.append(key)

    def get(self, key):
        """ Get an item by key """
        if key and key in self.cache_data:
            index = self.queue.index(key)
            del self.queue[index]
            self.queue.append(key)
            # print(f"XXXX {self.queue}")
            return self.cache_data[key]
        return None
