from django.urls import path,re_path
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name='sentiment'
urlpatterns = [
    path('', views.index, name='home'),
    path('about', TemplateView.as_view(template_name='sentiment/about.html'), name='about'),
    path('how_to', TemplateView.as_view(template_name='sentiment/how_to.html'), name='how_to'),
    path('export',csrf_exempt(views.export), name="export"),
    re_path(r'^search/$',views.searchQuery,name='searchQuery')   
]