from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_registration, name='home'),
    path('activate-account/', views.activate_account, name='activate-account')                               
]