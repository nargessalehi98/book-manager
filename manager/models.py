from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_date = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    cover_image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    num_pages = models.PositiveIntegerField(blank=True, null=True)
    subjects = models.TextField(blank=True, null=True)