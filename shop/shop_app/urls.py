from .views import *
from django.urls import path, include
from rest_framework import routers

router = routers.SimpleRouter()


urlpatterns = [
    path('', include(router.urls)),

    path('prediction/', SalesPrediction.as_view(), name='predict_sales'),
]
