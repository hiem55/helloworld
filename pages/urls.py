# pages/urls.py
from django.urls import path, include
from .views import homePageView, aboutPageView, namePageView, todos, register, message, logoutView, secretArea, results, submit_form

urlpatterns = [
    path('', homePageView, name='home'),
    path('about/', aboutPageView, name='about'),
    path('justin/', namePageView, name='justin'),
    path('todos/', todos, name='todos'),
    path("register/", register, name="register"),
    path('message/<str:msg>/<str:title>/', message, name="message"),
    path('', include("django.contrib.auth.urls")),
    path("logout/", logoutView, name="logout"),
    path("secret/", secretArea, name="secret"),
    path('results/<int:sq_ft>/<int:bedrooms>/<int:bathrooms>/<int:loc>', results, name='results'),  # New URL pattern
    path('submit/', submit_form, name='submit_form'),

]

