# Generated by Django 4.1.3 on 2023-05-11 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_alter_book_subjects'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='isbn',
        ),
        migrations.AddField(
            model_name='book',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
