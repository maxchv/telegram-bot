from django.contrib import admin
from .models import Dish, Category, Day, Order

# Register your models here.
admin.site.register(Dish)
admin.site.register(Category)
admin.site.register(Day)
admin.site.register(Order)
