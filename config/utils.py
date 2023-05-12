from config.requests import get_work_data, get_matching_book_data
from manager.models import Book


def build_cover_imager_url(cover_id: str):
    return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"


def get_book_extra_info(name: str):
    cover_imager_url, num_pages, subjects, description = "", "", "", ""
    work_id, num_pages, subjects = get_matching_book_data(name=name)
    if work_id:
        cover_id, description = get_work_data(work_id=work_id)
        if cover_id:
            cover_imager_url = build_cover_imager_url(cover_id)
    return num_pages, subjects, description, cover_imager_url


def update_book_status(book: Book):
    num_pages, subjects, description, cover_imager_url = get_book_extra_info(book.create_title_query())
    book.update_extra_info(num_pages, subjects, description, cover_imager_url)