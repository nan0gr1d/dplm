from django.shortcuts import render
from .models import Product
from .forms import ProductAdd

def homepage(request):
    """
    Функция отображает домашнюю страницу приложения
    :param request: - параметры запроса
    :return: - возвращает домашнюю страницу по шаблону home.html
    """
    return render(request, "home.html")


def catalog(request):
    """
    Функция отображения каталога товаров
    :param request: - параметры запроса
    :return: - возвращает страницу каталога товаров по шаблону catalog.html
    """
    products = Product.objects.all()
    context = {
        "products": products
    }
    return render(request, "catalog.html", context=context)


def process_form_data(title, price):
    """
    Функция проверки данных формы добавления товара
    :param title: - название товара
    :param price: - цена товара
    :return: - возвращает текстовое сообщение с диагностикой ошибки по результатам проверки.
            Если данные корректны, то возвращает пустое сообщение.
    """
    error = ''
    # Проверка цены товара на положительность
    if price <= 0:
        error = 'Product price must be positive number!'
        return error

    # Проверка названия товара на уникальность в каталоге
    products = Product.objects.all()
    for product in products:
        if title == product.title:
            error = f'Product {title} exists!'
            break
    return error


def add_product(request):
    """
    Функция добавления нового товара в каталог
    :param request: - параметры запроса
    :return: - возвращает форму добавления товара с сообщением о результате операции
    """
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


def delete_product(request):
    """
    Функция удаления товара из каталога по идентификатору
    :param request: - параметры запроса
    :return: - возвращает страницу каталога товара с сообщением о результате операции.
    """
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
