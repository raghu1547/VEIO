from django.urls import path
from . import views
urlpatterns = [
    path('security/', views.security, name='security'),
    path('security_officer/', views.securityOfficer, name='security_officer')
]
