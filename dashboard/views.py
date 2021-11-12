from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required,permission_required
from .models import Product,Order
from .forms import OrderForm, ProductForm
from django.contrib import messages
from .decorators import admin_only,salesman_only

# Create your views here.
@login_required()
def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    if request.method=='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.instance.staff = request.user
            form.save()
            return redirect('dashboard-index')
    else:
        form = OrderForm()
    context ={
        'orders':orders,
        'products':products,
        'form':form,
        'orders_count':orders.count(),
        'staff_count':User.objects.all().count(),
        'products_count':products.count(),
    }
    return render(request,'dashboard/index.html',context)

@login_required()
@permission_required('auth.view_user',login_url='dashboard-index')
def staff(request):
    users = User.objects.all()
    context = {
        'users':users,
        'orders_count':Order.objects.all().count(),
        'staff_count':users.count(),
        'products_count':Product.objects.all().count(),
    }
    return render(request,'dashboard/staff.html',context)

@login_required()
@permission_required('dashboard.view_order',login_url='dashboard-index')
def order(request):
    orders = Order.objects.all()
    context = {
        'orders':orders,
        'orders_count':orders.count(),
        'staff_count':User.objects.all().count(),
        'products_count':Product.objects.all().count(),
    }
    return render(request,'dashboard/order.html',context)

@login_required()
@permission_required('dashboard.add_product',login_url='dashboard-index')
def product(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request,f'{product_name} has been added!')
            return redirect('dashboard-product')
    else:
        form = ProductForm()
    context = {
        'products':products,
        'form':form,
        'orders_count':Order.objects.all().count(),
        'staff_count':User.objects.all().count(),
        'products_count':products.count(),
    }
    return render(request,'dashboard/product.html',context)

@login_required()
@permission_required('dashboard.delete_product',login_url='dashboard-index')
def product_delete(request,pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard-product')
    context = {
        'product':product
    }
    return render(request,'dashboard/product_delete.html',context)

@login_required()
@permission_required('dashboard.change_product',login_url='dashboard-index')
def product_update(request,pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm(instance=product)
    context = {
        'form':form
    }
    return render(request,'dashboard/product_update.html',context)

@login_required()
@permission_required('auth.view_user',login_url='dashboard-index')
def staff_view(request,pk):
    user = User.objects.get(id=pk)
    context = {
        'user':user
    }
    return render(request,'dashboard/staff_view.html',context)

@permission_required('dashboard.add_sales',login_url='dashboard-index')
def sales(request):
    return render(request,'dashboard/sales.html')

@permission_required('dashboard.add_purchase',login_url='dashboard-index')
def purchase(request):
    return render(request,'dashboard/purchase.html')

@permission_required('dashboard.add_accounts',login_url='dashboard-index')
def accounts(request):
    return render(request,'dashboard/accounts.html')