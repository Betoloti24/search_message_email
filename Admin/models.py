from django.db import models

class Usuario(models.Model):
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255)

    def __str__(self):
        return self.correo
