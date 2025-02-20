from django.urls import path
from . import views

urlpatterns = [
    path('', views.ingresar_correo, name='ingresar_correo'),
]
