#!/usr/bin/env python3
"""  LFU Caching"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ Defining  LFU Caching"""

    def __init__(self):
        super().__init__()
        self.queue = {}

    def put(self, key, item):
        """ Add an item in the cache"""
        if key and item:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS and \
                    key not in self.cache_data:
                min_key = min(self.queue, key=lambda k: self.queue[k])
                del self.queue[min_key]
                del self.cache_data[min_key]
                print(f"DISCARD: {min_key}")

            self.cache_data[key] = item
            # Increment the count associated with the key in the queue
            self.queue[key] = self.queue.get(key, 0) + 1

    def get(self, key):
        """ Get an item by key """
        if key and key in self.cache_data:
            self.queue[key] = self.queue.get(key, 0) + 1
            # print(f"XXXX {self.queue}")
            return self.cache_data[key]
        return None
