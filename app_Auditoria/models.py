from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Genero(models.Model):
    descripcion_Genero = models.CharField(max_length=20, null = False,blank=False)
    
    def __str__(self):
        return "{}-{}".format(self.pk,self.descripcion_Genero)

class Paciente(models.Model):
    identidad = models.CharField(max_length=100, null = False,blank=False)
    nombres = models.CharField(max_length=100, null = False,blank=False)
    apellidos = models.CharField(max_length=100, null = False,blank=False)
    genero = models.ForeignKey(Genero,on_delete=models.CASCADE, null=False,blank=False)
    telefono = models.CharField( max_length=50)
    direccion= models.CharField( max_length=100)
    fecha_registro = models.DateField( auto_now_add=True)

    def __str__(self):
        return "{}-{}-{}-{}-{}".format(self.pk,self.identidad,self.nombres,self.apellidos,self.fecha_registro)

class Doctor(models.Model):
    identidad = models.CharField(max_length=100, null = False,blank=False)
    nombres = models.CharField(max_length=100, null = False,blank=False)
    apellidos = models.CharField(max_length=100, null = False,blank=False)
    genero = models.ForeignKey(Genero,on_delete=models.CASCADE, null=False,blank=False)
    telefono = models.CharField( max_length=50)
    correo = models.CharField(max_length=100, null = False,blank=False)
    direccion= models.CharField( max_length=100)
    fecha_registro = models.DateField( auto_now_add=True)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE, null=False,blank=False)

    def __str__(self):
        return "{}-{}-{}-{}-{}-{}".format(self.pk,self.identidad,self.nombres,self.apellidos,self.correo,self.fecha_registro)

class Cita(models.Model):
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE, null=False,blank=False)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE, null=False,blank=False)
    fecha_registro = models.DateField( auto_now_add=True)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE, null=False,blank=False)
    estado= models.BooleanField(null = False, blank = False)

    def __str__(self):
        return "{}-{}-{}-{}-{}-{}".format(self.pk,self.paciente,self.doctor,self.fecha_registro,self.estado,self.doctor.usuario.pk)

class Asiganacion_Cita(models.Model):
    cita = models.ForeignKey(Cita,on_delete=models.CASCADE, null=False,blank=False)
    fecha_registro = models.DateField( auto_now_add=True)
    

    def __str__(self):
        return "{}-{}-{}".format(self.pk,self.cita,self.fecha_registro)

class Expediente(models.Model):
    cita = models.ForeignKey(Cita,on_delete=models.CASCADE, null=False,blank=False)
    diagnostico= models.CharField( max_length=100, null=False,blank=False)
    tratamiento= models.CharField( max_length=100, null=False,blank=False)
    fecha_registro = models.DateField( auto_now_add=True)
    paciente = models.CharField(max_length=100, null = False,blank=False)
    doctor = models.CharField(max_length=100, null = False,blank=False)
    
    def __str__(self):
        return "{}-{}-{}-{}-{}".format(self.pk,self.cita,self.fecha_registro,self.paciente,self.doctor)