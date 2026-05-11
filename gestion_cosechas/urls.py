from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('fundos/', views.fundos, name='fundos'),
    path('formulario/', views.registro_kilos, name='registro_kilos'),
    path('personal/supervisor/', views.formulario_supervisor, name='supervisor'),
    path('personal/cosechero/', views.formulario_cosechero, name='cosechero'),
]