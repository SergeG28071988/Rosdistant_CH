from django.contrib import admin
from .models import Product
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'amount')
    fields = ['name', 'description', 'price', 'quantity', 'category', 'date_of_receipt']
