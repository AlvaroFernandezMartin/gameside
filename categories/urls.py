from django.urls import path

from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.categorie_list, name='category-list'),
    path('<slug>/', views.categorie_detail, name='category-detail'),
]
