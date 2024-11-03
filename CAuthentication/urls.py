from django.urls import path
from . import views

app_name='CAuthentication'

urlpatterns = [
    path('login/', views.login_page, name='login')
]
