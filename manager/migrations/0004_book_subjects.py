# Generated by Django 4.1.3 on 2023-05-11 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_alter_book_isbn'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='subjects',
            field=models.TextField(blank=True, null=True),
        ),
    ]
