from django.db import models
from django.contrib.auth.models import User

class Archives(models.Model):
    dat = models.DateField()
    eur = models.FloatField(default=0, blank=True)
    usd = models.FloatField(default=0, blank=True)
    rub = models.FloatField(default=0, blank=True)

class ValueErrorException(Exception):
    pass

class EmptyValueException(Exception):
    pass

class DateDoesNotExistYet(Exception):
    pass