# Generated by Django 3.2.5 on 2021-07-13 03:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sentiment', '0005_auto_20210704_1030'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='searchentries',
            options={'ordering': ('-search_date', '-search_time')},
        ),
    ]