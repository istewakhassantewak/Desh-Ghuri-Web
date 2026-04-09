from django.urls import path
from .views import register,handlelogout,handle_login

urlpatterns = [
    path('register/', register, name='register'),

    path('logout/', handlelogout, name='logout'),
    path('login/', handle_login, name='login'),

]

