from django.contrib import admin
from .models import Fruit


class FruitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


# Register your models here.
admin.site.register(Fruit, FruitAdmin)