from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from order.models import Order


@shared_task
def payment_completed(order_id):
    """
        task to send an email nofification for the user when the task is successfuly 
        created and the payment is completed

    """
    order = Order.objects.get(id = order_id)
    #create invoice email
    subject = f'Khaled Osman Shop - EE Invoice no. {order.id}'
    message = 'please , find the attached invoice file for your recent purchase'
    email = EmailMessage(subject, 
                         message,
                         'admin@myshop.com',
                         [order.email]
                            )
    #generate pdf
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_DIR + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,
                                           stylesheets=stylesheets)

    #attach the pdf file to the email
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    #send email
    email.send()
