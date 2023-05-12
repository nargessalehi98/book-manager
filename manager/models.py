from django.db import models


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
        self.set_subject_list(subjects)
        self.description = description
        self.cover_image_url = cover_imager_url
        self.updated = True
        self.save()
