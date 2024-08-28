from decimal import Decimal
from django.db import models

PROFIT_MARGIN = Decimal(0.08)

# Create your models here.
class Observation(models.Model):
    updated_at = models.DateTimeField(auto_now= True)
    date = models.DateField()
    description = models.CharField(max_length= 200)

    def __str__(self):
        return f'DATE: ${self.date} - DESCRIPTION: {self.description}'