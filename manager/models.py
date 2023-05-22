from django.db import models

from config.celery_tasks import update_db_instance


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_date = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    cover_image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    num_pages = models.PositiveIntegerField(blank=True, null=True)
    subjects = models.CharField(blank=True, max_length=1000)
    updated = models.BooleanField(default=False)
    task_id = models.CharField(max_length=255, blank=True, null=True)

    # objects = models.Manager()
    # not_update_objects = NotUpdateManager()
    # fill up with is_updated = False

    def is_updated(self):
        return self.updated

    def set_subject_list(self, value):
        self.my_list = ','.join(value) if value else None

    def get_subject_list(self):
        return self.my_list.split(',')

    def create_title_query(self):
        return self.title.replace(" ", "+")

    def update_extra_info(self, num_pages, subjects, description, cover_imager_url):
        self.num_pages = num_pages
        self.subjects = ','.join(subjects) if subjects else None
        self.description = description
        self.cover_image_url = cover_imager_url
        self.updated = True
        self.save()

    def save(self):
        task_id = update_db_instance.delay(self)
        self.task_id = task_id
        super().save()