from rest_framework import serializers
from .models import Category, Dish, Day, Order


class DaySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Day
        fields = 'id', 'day', 'dishes'


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = 'id', 'name'


class DishSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Dish
        fields = 'id', 'name', 'weight', 'price', 'category'


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Order
        fields = 'id', 'date', 'dishes',  'client_id', 'address'
