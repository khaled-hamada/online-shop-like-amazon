from django.contrib import admin
from django.contrib.admin.decorators import action
from  .models import Category, Product
# Register your models here.
from faker import Faker
from decimal import Decimal
from random import randint
from django.utils.text import slugify

def add_100_categories(modeladmin, request, queryset ):
    fake = Faker()
    names = [fake.unique.first_name() for i in range(100)]
    cat = [Category(name=name, slug=slugify(name)) for name in names]
    Category.objects.bulk_create(cat)

def add_1000_products(modeladmin, request, queryset ):
    fake = Faker()
    names = [f'{fake.first_name()},{i}' for i in range(1000)]
    cat_qs = Category.objects.all()
    count = cat_qs.count()
    products = [
        Product(name=name,
               slug = slugify(name),
               price=fake.pydecimal(4, 2, True),
               category=cat_qs[randint(0, count-1 )])
        for name in names
        ]
    Product.objects.bulk_create(products)

def products_count(obj):
    return obj.products.all().count()
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', products_count]
    prepopulated_fields = {'slug': ('name',)}
    actions = [add_100_categories]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    actions = [add_1000_products]
