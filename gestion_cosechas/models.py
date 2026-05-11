from django.db import models

class Fundo(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)

class Supervisor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    contrasena = models.CharField(max_length=255)
    fundo = models.ForeignKey(Fundo, on_delete=models.SET_NULL, null=True)

class Cosechero(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    nacionalidad = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    cuadrilla = models.CharField(max_length=50)