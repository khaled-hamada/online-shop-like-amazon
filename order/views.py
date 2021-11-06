from django.shortcuts import render

from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form  = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            items = [
                OrderItem(
                    order = order,
                    product= item['product'],
                    price = item['price'],
                    quantity = item['quantity']
                )
                for item in cart
            ]
            OrderItem.objects.bulk_create(items)
            #clear the cart
            cart.clear()
            return render(request, 'orders/order/created.html',
                            {
                                'order':order
                            })
    else:
        form = OrderCreateForm()
    return render(request, 
                'orders/order/create.html',
                {
                    'cart':cart,
                    'form':form
                }
                )