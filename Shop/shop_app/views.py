from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product
# Create your views here.



def index(request):    
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {'title': 'Главная страница сайта', 'num_visits': num_visits}
    return render(request, 'index.html', context)


def products(request):
    products = Product.objects.all()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {'title': 'Товары', 'products': products, 'num_visits': num_visits}
    return render(request, 'product_list.html', context)


def create(request):
    error = ''
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        else:
            error = "Форма была не верной"
    form = ProductForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'create.html', context)
