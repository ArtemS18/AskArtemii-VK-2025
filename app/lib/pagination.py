from math import ceil
from typing import NamedTuple
from starlette.requests import Request

WINDOW = 10


def get_offset(total, page, per_page: int = 5):
    if page < 1:
        page = 1 
    pages = max(1, ceil(total / per_page))
    if page > pages:
        page = pages
    start = (page - 1) * per_page
    return start

class PaginateData(NamedTuple):
    offset: int
    page: int
    pages: int
    has_prev: bool
    has_next: bool
    prev_page: int
    next_page: int
    
    window_range: range
    has_prev_chunk: bool
    has_next_chunk: bool
    prev_chunk_page: int
    next_chunk_page: int

def paginate(total: int, page: int =1, per_page: int = 5):
    try:
        page = int(page)
    except (TypeError, ValueError):
        page = 1
    if page < 1:
        page = 1 
    pages = max(1, ceil(total / per_page))
    if page > pages:
        page = pages
    start = (page - 1) * per_page

    has_prev = page > 1
    has_next = page < pages
    prev_page = page - 1 if has_prev else None
    next_page = page + 1 if has_next else None

    chunk_index = (page - 1) // WINDOW
    first_in_window = chunk_index * WINDOW + 1
    last_in_window = min(first_in_window + WINDOW - 1, pages)
    window_range = range(first_in_window, last_in_window + 1)
    has_prev_chunk = first_in_window > 1
    has_next_chunk = last_in_window < pages
    prev_chunk_page = max(1, first_in_window - WINDOW)
    next_chunk_page = min(pages, first_in_window + WINDOW)

    return PaginateData(
        offset=start,
        page=page,
        pages=pages,
        has_prev=has_prev,
        has_next=has_next,
        prev_page=prev_page,
        next_page=next_page,
        
        window_range=window_range,
        has_prev_chunk=has_prev_chunk,
        has_next_chunk=has_next_chunk,
        prev_chunk_page=prev_chunk_page,
        next_chunk_page=next_chunk_page,
    )
