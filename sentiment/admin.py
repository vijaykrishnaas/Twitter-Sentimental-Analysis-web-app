from django.contrib import admin

# Register your models here.
from .models import SearchEntries


class MyAdmin(admin.ModelAdmin):
    list_display = ("search_query", "query_date", "search_time",
                    "search_date", "user_host", "user_agent")
    list_filter = ("search_date", "search_time")


admin.site.register(SearchEntries, MyAdmin)
admin.site.site_header = "Twitter Sentiment Admin Dashboard"
