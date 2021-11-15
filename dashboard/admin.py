from django.contrib import admin
from .models import Accounts, Product,Order, Purchase, Sales
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','category','quantity')
    list_filter = ('category',)
admin.site.site_header='Inventory System'
admin.site.register(Product,ProductAdmin)
admin.site.register(Order)
admin.site.register(Purchase)
admin.site.register(Sales)
admin.site.register(Accounts)