# Generated by Django 4.1.6 on 2023-04-13 05:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0003_blogpost_maintitle'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpost',
            old_name='tilte',
            new_name='title',
        ),
    ]