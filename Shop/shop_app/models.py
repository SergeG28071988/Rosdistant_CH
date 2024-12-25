from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100, help_text="Введите наименование товара", verbose_name="Товар")
    description = models.CharField(max_length=500, help_text="Введите описание товара", verbose_name="Описание товара")
    price = models.DecimalField(help_text="Введите цену товара", verbose_name="Цена товара", 
                                max_digits=10,
                                decimal_places=2)
    quantity = models.IntegerField(verbose_name="Кол-во товара")
    amount = models.DecimalField(help_text="Итоговая стоимость товара", verbose_name="Итоговая стоимость", 
                                max_digits=10,
                                decimal_places=2) # считается как произведение price * quantity 
    CATEGORY_CHOICES = [
        ('Сосиски', 'Сосиски'),
        ('Колбаса', 'Колбаса'),
        ('Яблоки', 'Яблоки'),
        ('Киви', 'Киви'),
        ('Виноград', 'Виноград'),       
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Категория товара')
    date_of_receipt = models.DateField(help_text='Введите дату добавления', 
                                       verbose_name='Дата добавления', 
                                       null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Рассчитываем итоговую стоимость
        self.amount = self.price * self.quantity
        super().save(*args, **kwargs)  # Вызываем родительский метод save    
    
    def __str__(self): 
         return f'Наименование: {self.name} Описание: {self.description}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        