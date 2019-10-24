from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from .models import Category, Dish, Day, Order
from .serializers import CategorySerializer, DishSerializer, DaySerializer, OrderSerializer


class DayViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DaySerializer

    def get_queryset(self):
        queryset = Day.objects.all().order_by('-day')
        day = self.request.query_params.get('day', None)
        if day is not None:
            queryset = Day.objects.filter(day=day)
        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DishViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

