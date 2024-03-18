# pages/urls.py
from django.urls import path
from .views import homePageView, aboutPageView, namePageView

urlpatterns = [
    path('', homePageView, name='home'),
    path('about/', aboutPageView, name='about'),
    path('justin/', namePageView, name='justin')
]
