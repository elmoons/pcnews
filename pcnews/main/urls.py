from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.registorPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('contacts', views.contacts, name='contacts'),
]