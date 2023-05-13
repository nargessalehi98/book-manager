# Generated by Django 4.1.3 on 2023-05-11 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='id',
        ),
        migrations.RemoveField(
            model_name='book',
            name='subjects',
        ),
        migrations.AddField(
            model_name='book',
            name='isbn',
            field=models.TextField(default=11, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
