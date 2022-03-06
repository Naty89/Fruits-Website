from django.db import models
from tastypie.resources import ModelResource
from App.models import Fruit
# Create your models here.


class FruitResources(ModelResource):
    class Meta:
        queryset = Fruit.objects.all()
        resource_name = 'fruits'