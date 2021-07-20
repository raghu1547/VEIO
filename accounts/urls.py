from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('checkUser/', views.checkUser, name="checkUser"),
    path('logout/', views.logout, name="logout")
]
