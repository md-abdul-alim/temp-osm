from django.urls import path
from .views import OrderCreateAPI, OrderDetailAPI, CustomerReportAPI

urlpatterns = [
    path('orders/create/', OrderCreateAPI.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderDetailAPI.as_view(), name='order-detail'),
    path('customers/<int:pk>/report/', CustomerReportAPI.as_view(), name='customer-report'),
]
