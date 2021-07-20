from django.urls import path
from . import views
urlpatterns = [
    path('checkReg/', views.checkReg, name='checkReg')
]
