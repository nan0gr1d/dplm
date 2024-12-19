from django.shortcuts import render
from .models import Product
from .forms import ProductAdd


def homepage(request):
    return render(request, "home.html")

def catalog(request):
    products = Product.objects.all()
    context = {
        "products": products
    }
    return render(request, "catalog.html", context=context)

def process_form_data(title, price):
    error = ''
    if int(price) <= 0:
        error = 'Product price must be positive number!'
        return error

    products = Product.objects.all()
    for product in products:
        if title == product.title:
            error = f'Product {title} exists!'
            break
    return error

def add_product(request):
    error = ''
    if request.method == 'POST':
        form = ProductAdd(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            price = int(form.cleaned_data['price'])
            error = process_form_data(title, price)
            if not error:
                Product.objects.create(title=title, description=description, price=price)
                message = f"Product {title} added."
                context = {
                    'message': message,
                }
                return render(request, 'home.html', context=context)
    else:
        form = ProductAdd()
    context = {
        'form': form,
        'error': error,
    }
    return render(request, 'product_add.html', context=context)

def delete_product(request):
    id = request.POST.get("id")
    product = Product.objects.get(id=id)
    if product:
        title = product.title
        product.delete()
        message = f"Product {title} (id={id}) deleted."
    else:
        message = f"Product (id={id}) not found."
    context = {
                'message': message,
                }
    return render(request, 'home.html', context=context)
