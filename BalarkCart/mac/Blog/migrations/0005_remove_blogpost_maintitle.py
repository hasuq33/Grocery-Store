# Generated by Django 4.1.6 on 2023-04-13 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0004_rename_tilte_blogpost_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='maintitle',
        ),
    ]
