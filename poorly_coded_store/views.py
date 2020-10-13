from django.shortcuts import render, redirect
from .models import Order, Product
from django.db.models import Sum

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request):

    context = {
        'order': Order.objects.last(),
        'total_price_for_all_orders': Order.objects.aggregate(Sum('total_price')),
        'total_quantity_for_all_orders':Order.objects.aggregate(Sum('quantity_ordered'))
    }

    return render(request, "store/checkout.html", context)

def calculations(request):
    product = Product.objects.get(id=request.POST['product_id'])
    price_of_product = product.price
    quantity_from_form = int(request.POST["quantity"])
    total_charge = quantity_from_form * price_of_product
    print("Charging credit card...")
    Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)
    return redirect('/checkout')