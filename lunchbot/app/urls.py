from django.urls import path, include
from rest_framework import routers
from .views import CategoryViewSet, DishViewSet, DayViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'dishes', DishViewSet)
router.register(r'days', DayViewSet, basename='day')
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls))
]
