from django.db import models


from apps.authentication.models import CustomUser

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)

    def __str__(self):
        return self.name
    

class Boat(models.Model):
    supplier = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    name = models.CharField(max_length= 100)

    def __str__(self):
        return self.name