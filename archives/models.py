from django.db import models

class Archives(models.Model):
    dat = models.DateField()
    eur = models.FloatField(default=0, blank=True)
    usd = models.FloatField(default=0, blank=True)
    rub = models.FloatField(default=0, blank=True)