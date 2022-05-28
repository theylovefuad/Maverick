from django.contrib import admin

# Register your models here.
from .models import Item, OurDishes

admin.site.register(Item)
admin.site.register(OurDishes)


