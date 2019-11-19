from django.contrib import admin
from .models import Dish, Category, Day, Order

# Register your models here.
admin.site.register(Category)
admin.site.register(Day)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'weight')
    ordering = ('category',)
    list_filter = ('category',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('date', 'address', 'client_id', 'completed')
    ordering = ('-date', 'client_id')
    list_filter = ('date', 'completed', 'address')
