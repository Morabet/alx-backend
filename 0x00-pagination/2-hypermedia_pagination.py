#!/usr/bin/env python3
"""Hypermedia pagination"""

import csv
import math
from typing import List, Tuple, Dict


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Retrieves the index range from a given page and page size"""

    start_index = (page - 1) * page_size
    end_index = page * page_size
    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Retrieves a page of data"""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size >= 0
        data = self.dataset()
        start, end = index_range(page, page_size)
        if start > len(data):
            return []
        return data[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """Retrieves information about a page"""
        page = page
        data = self.get_page(page, page_size)
        data_len = len(self.__dataset)
        total_pages = math.ceil(data_len / page_size)

        next_page = page + 1 if page + 1 <= total_pages else None
        prev_page = page - 1 if 2 <= page else None

        return {"page_size": len(data), "page": page,
                "data": data, "next_page": next_page,
                "prev_page": prev_page, "total_pages": total_pages}
