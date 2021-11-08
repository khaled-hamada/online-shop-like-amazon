import braintree

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings 
from order.models import Order
from .tasks import payment_completed
#instantiate the braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        #retrieve nonce token 
        nonce = request.POST.get('payment_method_nonce', None)
        # print(nonce)
        # create and submit transaction
        result = gateway.transaction.sale(
            {
                'amount':f'{total_cost:.2f}',
                'payment_method_nonce':nonce,
                'options':{
                    'submit_for_settlement':True,
                }
            }
        )
        # print(result)
        if result.is_success:
            #mark  the order as paid
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            #send emial confirmation to user
            payment_completed.delay(order.id)
            del request.session['order_id']
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        #generate token
        client_token = gateway.client_token.generate()
        # print('client token:', client_token)
        return render(request, 'payment/process.html',{
                'order':order,
                'client_token':client_token,
            })



def payment_done(request):
    return render(request, 'payment/done.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')