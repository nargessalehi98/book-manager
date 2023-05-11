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

    def set_subject_list(self, value):
        self.my_list = ','.join(value)

    def get_subject_list(self):
        return self.my_list.split(',')
