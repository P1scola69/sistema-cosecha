from django.db import models

class Fundo(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        db_table = 'fundos' 

class Cosechero(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    nacionalidad = models.CharField(max_length=50, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    cuadrilla = models.CharField(max_length=50, null=True, blank=True)
    class Meta:
        db_table = 'cosecheros'

class Supervisor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    correo = models.EmailField(max_length=100, unique=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    contrasena = models.CharField(max_length=255)
    fundo = models.ForeignKey(Fundo, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        db_table = 'supervisores'

class RegistroKilo(models.Model):
    fundo = models.ForeignKey(Fundo, on_delete=models.CASCADE)
    cosechero = models.ForeignKey(Cosechero, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    variedad = models.CharField(max_length=50)
    kilos = models.DecimalField(max_digits=7, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'registro_kilos'