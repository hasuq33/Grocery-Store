# Generated by Django 4.1.6 on 2023-04-13 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='publisher',
            field=models.CharField(default='', max_length=50),
        ),
    ]
