# Generated by Django 3.2.5 on 2021-07-03 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchEntries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=20)),
                ('user_name', models.CharField(max_length=20)),
                ('search_query', models.CharField(max_length=50)),
                ('query_date', models.CharField(max_length=20)),
                ('user_host', models.CharField(max_length=20)),
                ('user_agent', models.CharField(max_length=100)),
            ],
        ),
    ]
