from django.shortcuts import render
from .models import Product
from .forms import ProductAdd

# Отображаем домашнюю страницу
def homepage(request):
    return render(request, "home.html")

# Отображаем каталог товаров
def catalog(request):
    products = Product.objects.all()
    context = {
        "products": products
    }
    return render(request, "catalog.html", context=context)

# Обрабатываем данные из формы добавления товара
def process_form_data(title, price):
    error = ''
    if price <= 0:
        error = 'Product price must be positive number!'
        return error

    products = Product.objects.all()
    for product in products:
        if title == product.title:
            error = f'Product {title} exists!'
            break
    return error


# Добавляем новый товар в каталог
def add_product(request):
    message = ''
    if request.method == 'POST':
        form = ProductAdd(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            price = float(form.cleaned_data['price'])
            # Проверка корректности введенных данных
            error = process_form_data(title, price)
            if error:
                message = error
            else:
                Product.objects.create(title=title, description=description, price=price)
                message = f"Product {title} added."
    else:
        form = ProductAdd()
    context = {
        'form': form,
        'message': message,
    }
    return render(request, 'product_add.html', context=context)

# Удаляем товар из каталога по идентификатору
def delete_product(request):
    id = request.POST.get("id")
    # Есть ли товар с указанным идентификатором в каталоге?
    product = Product.objects.get(id=id)
    if product:
        title = product.title
        product.delete()
        message = f"Product {title} (id={id}) deleted."
    else:
        message = f"Product (id={id}) not found."
    products = Product.objects.all()
    context = {
                'message': message,
                'products': products
                }
    return render(request, 'catalog.html', context=context)
