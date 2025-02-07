from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('add/', views.add_order, name='add-order'),
    path('<int:pk>/', views.order_detail, name='order-detail'),
]
