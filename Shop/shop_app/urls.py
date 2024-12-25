from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),   
    path('products/', views.products, name='product_list'),  
    path('create', views.create, name='create'),
]
