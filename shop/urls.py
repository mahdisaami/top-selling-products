from django.urls import path
from shop.views import TopSellingProductsAPIView

urlpatterns = [
    path('top-selling-products/', TopSellingProductsAPIView.as_view(), name='top-selling'),
]
