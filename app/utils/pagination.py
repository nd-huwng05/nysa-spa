import math


class Pagination:
    def __init__(self, page_index, per_page, total_items):
        self.page_index = page_index
        self.per_page = per_page
        self.total_items = total_items

        self.total_pages = math.ceil(self.total_items / self.per_page) if per_page > 0 else 0

    def to_dict(self):
        return {
            'index': self.page_index,
            'per_page': self.per_page,
            'total_page': self.total_pages,
        }