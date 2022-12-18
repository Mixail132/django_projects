from django.db import models

class Archives(models.Model):
    dat  = models.DateField()
    eur  = models.FloatField()
    usd  = models.FloatField()