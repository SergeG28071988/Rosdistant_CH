from django.forms import ModelForm, TextInput, DateInput, NumberInput, Select
from .models import Product  

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "quantity", "category", "date_of_receipt"]  # Убрали amount
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите товар'
            }),
            "description": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание товара'
            }),
            "price": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите цену товара'
            }),
            "quantity": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите кол-во товара'
            }),
            "category": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Выберите категорию товара'
            }),
            "date_of_receipt": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите дату поступления товара',
                'type': 'date'  # Указываем тип date для календаря
            })           
        }

    def save(self, commit=True):
        product = super().save(commit=False)
        product.amount = product.price * product.quantity  # Рассчитываем amount
        if commit:
            product.save()
        return product
