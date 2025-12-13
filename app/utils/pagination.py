import math


class Pagination:
    page: int
    size: int

    def __init__(self, page, size, page_size_default=10):
        self.page_size_default = page_size_default
        self.page = page
        self.size = size

    def format(self):
        if self.size == 0:
            self.size = self.page_size_default

        if self.size < 0:
            self.size = 1

        if self.page <= 0:
            self.page = 1

    def offset(self) -> int:
        self.format()
        return (self.page - 1) * self.size

    def total_pages(self, total: int) -> int:
        if total == 0:
            return 0

        total_pages = int(math.ceil(float(total + self.page - 1) / float(self.size)))
        if total > 0 and total_pages == 0:
            return 1

        return total_pages

    def to_dict(self, total_items:int):
        return {
            'page': self.page,
            'limit': self.size,
            'total_pages': self.total_pages(total_items),
        }