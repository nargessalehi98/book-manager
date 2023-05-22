from config.celery import app
from celery.signals import celeryd_init

from config.utils import get_book_extra_info
from manager.models import Book

# How this one is working?
# CeleryBeats --> CRON JOB FOR CELERY
# Update on save function of the model


class CeleryTasks:
    @staticmethod
    @app.task
    def update_db():
        books = Book.objects.filter(updated=False)
        for book in books:
            num_pages, subjects, description, cover_imager_url = get_book_extra_info(book.create_title_query())
            book.update_extra_info(num_pages, subjects, description, cover_imager_url)


@celeryd_init.connect
def configure_workers(*args, **kwargs):
    CeleryTasks.update_db.delay()


@app.task
def update_db_instance(book):
    num_pages, subjects, description, cover_imager_url = get_book_extra_info(book.create_title_query())
    book.update_extra_info(num_pages, subjects, description, cover_imager_url)