from rest_framework import serializers
from .models import Category, Dish, Day, Order


class DaySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Day
        fields = '__all__'


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class DishSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Dish
        fields = '__all__'


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
