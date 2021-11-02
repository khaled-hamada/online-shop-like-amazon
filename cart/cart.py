from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):
    """ this is class will be used to create and manage shop carts """

    def __init__(self, request):
        """ Initialize the Cart"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart
    
    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
            

    def __len__(self):
        "count all items quantities not just products count"
        return sum(item['quantity'] for item in self.cart.values())


    def add(self, product, quantity=1, override_quantity= False):
        """
            add a new product to the cart or updating an existing one
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0, 
                                     'price':str(product.price)}
            
            if override_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
        #update session data
        self.save()

    def save(self):
        # mark session as modified to make sure its get updated 
        self.session.modified = True
        
    def remove(self, product):
        product_id = str(product.id)
        del self.cart[product_id]
        self.save()
    
    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())