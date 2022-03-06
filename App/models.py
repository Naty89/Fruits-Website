from django.db import models


# Create your models here.
class Fruit(models.Model):
    name = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    img = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.name