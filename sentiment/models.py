from django.db import models

# Create your models here.


class SearchEntries(models.Model):
    user_id = models.CharField(max_length=20)
    user_name = models.CharField(max_length=20)
    search_query = models.CharField(max_length=50)
    query_date = models.CharField(max_length=20)
    user_host = models.CharField(max_length=20)
    user_agent = models.CharField(max_length=100)
