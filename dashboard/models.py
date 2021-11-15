from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
CATEGORY = (
    ('Stationary','Stationary'),
    ('Electronics','Electronics'),
    ('Food','Food'),
)

class Product(models.Model):
    name = models.CharField(max_length=100,null=True)
    category = models.CharField(max_length=20,choices=CATEGORY,null=True)
    quantity = models.PositiveIntegerField(null=True)

    def __str__(self) -> str:
        return f'{self.name}-{self.quantity}'

class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    staff = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.product} ordered by {self.staff.username}'

class Purchase(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    supplier_name = models.CharField(max_length=50,null=True)
    price_per = models.PositiveIntegerField(null=True)
    quantity = models.PositiveIntegerField(null=True)
    total_price = models.IntegerField(null=True)
    date = models.DateTimeField(default=timezone.now())
    def __str__(self):
        return f'{self.product.name} '

class Sales(models.Model):
    purchase = models.ForeignKey(Purchase,on_delete=models.CASCADE,null=True)
    customer_name = models.CharField(max_length=50,null=True)
    price_per = models.PositiveIntegerField(null = True)
    quantity = models.PositiveIntegerField(null=True)
    total_price = models.IntegerField(null=True)
    date = models.DateTimeField(default=timezone.now())
    def __str__(self) :
        return f'{self.purchase} price {self.sales_price}'

class Accounts(models.Model):
    sales = models.OneToOneField(Sales,on_delete=models.CASCADE,null=True)
    purchase_price = models.PositiveIntegerField(null=True)
    profit_price = models.IntegerField(null=True)