from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.core.paginator import Paginator, EmptyPage, InvalidPage

def allProdCat(request, c_slug=None):
    c_page = None
    products_list = None
    page = None  # Define page variable with a default value

    if c_slug is not None:
        c_page = get_object_or_404(Category, slug=c_slug)
        products_list = Product.objects.filter(category=c_page, available=True)
    else:
        products_list = Product.objects.filter(available=True)
        paginator = Paginator(products_list, 6)
        page_number = request.GET.get('page', 1)
        try:
            page = paginator.page(page_number)
        except (EmptyPage, InvalidPage):
            page = paginator.page(paginator.num_pages)

    return render(request, "category.html", {'category': c_page, 'products': page if page else products_list})

def prodDetail(request, c_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=c_slug, slug=product_slug)
        return render(request, 'products.html', {'product': product})
    except Exception as e:
        raise e

def cart_view(request):
    return HttpResponse("This is the cart view.")