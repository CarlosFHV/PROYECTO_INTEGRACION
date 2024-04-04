from django.db import models

class textos_informacion(models.Model):
    texto_original = models.TextField()
    texto_procesado = models.TextField()
    analisis_sentimiento = models.FloatField()  # Usamos FloatField para almacenar un número decimal
    etiqueta = models.CharField(max_length=50)
    rango_izq = models.FloatField()
    rango_der = models.FloatField()