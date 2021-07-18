from django.db import models

# Create your models here.


class SearchEntries(models.Model):
    search_query = models.CharField(max_length=50, default="")
    query_date = models.CharField(max_length=20, default="")
    search_time = models.TimeField(null=True, blank=True)
    search_date = models.DateField(null=True, blank=True)
    user_host = models.CharField(max_length=50, default="")
    user_agent = models.CharField(max_length=250, default="")

    class Meta:
        ordering = ("-search_date", "-search_time")

    def __str__(self):
        return f"{self.search_query}, {self.query_date}, {self.search_time}, {self.search_date}, {self.user_host}, {self.user_agent}"
