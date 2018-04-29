from django.conf.urls import url
from DataFetcher import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
]