from django.db import models

class Albaran(models.Model):
    archivo = models.CharField(max_length=255)
    numero = models.CharField(max_length=255, null=True, blank=True)
    fecha = models.CharField(max_length=255, null=True, blank=True)
    proveedor = models.CharField(max_length=255, null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.archivo} - {self.numero}"
