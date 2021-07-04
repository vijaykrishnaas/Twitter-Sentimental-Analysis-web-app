from django import forms
from django import forms
from .models import SearchEntries


class SearchEntriesForm(forms.ModelForm):
    class Meta:
        model = SearchEntries
        fields = ["search_query", "query_date", "search_time",
                  "search_date", "user_host", "user_agent"]
