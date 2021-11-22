from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required,permission_required
from .models import Accounts, Customer, Product,Order, Purchase, Sales
from .forms import AccountsForm, BSModalPurchaseUpdateForm, OrderForm, ProductForm, PurchaseForm, PurchaseUpdateForm, SalesForm, SalesUpdateForm,BSModalSalesUpdateForm
from django.contrib import messages
from .decorators import admin_only,salesman_only
from bootstrap_modal_forms.generic import BSModalReadView, BSModalUpdateView
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
        'purchase':Purchase.objects.all()
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
    search_value=''
    total_sold_price = 0 
    sales = Sales.objects.all().order_by('-date')
    if request.method=='POST':
        form = SalesForm(request.POST)
        customer_name = request.POST.get('customer_name')
        if form.is_valid():
            sales = form.save(commit=False)
            sales_quantity  = sales.quantity
            purchase_quantity = sales.purchase.quantity
            purchase = sales.purchase
            available_stock = purchase_quantity-sales_quantity
            purchase.quantity = available_stock
            if available_stock >= 0:
                sales.save()
                purchase.save()
                #If Custemer name is exsist save the sales detail in customer
                #If customer name is not exsits create a new customer and save the sales detail in newly created customer
                
                try:
                    customer = Customer.objects.get(name=customer_name)
                    customer.sale.add(sales)
                except Customer.DoesNotExist:
                    customer = Customer(name=customer_name)
                    customer.save()
                    customer.sale.add(sales)
            else:
                #form error
                messages.error(request, "The Product Out of Stock")
            return redirect('dashboard-sales')
    
    else:
        for sale in sales:
            print(sale.customer_set.all())
        form = SalesForm()
        
        search = request.GET.get('search')
        if search:
            sales = Sales.objects.filter(purchase__product__name__icontains=search).order_by('-date')
            search_value = search
    for sale in sales:
        total_sold_price+=sale.total_price
    context = {
        'form':form,
        'sales_list':sales,
        'total_sold_price':total_sold_price,
        'search_value':search_value,
        'customers':Customer.objects.all()
    }
    return render(request,'dashboard/sales.html',context)

def customer_autocomplete(request):
    # data = Customer.objects.all().values_list('name',flat=True)
    # json = list(data)
    # return JsonResponse(json, safe=False)
    if request.GET.get('customer_name'):
        customer_name = request.GET['customer_name']
        data = Customer.objects.filter(name__startswith=customer_name).values_list('name',flat=True)
        json = list(data)
        return JsonResponse(json, safe=False)
    else:
        return HttpResponse("No cookies")

@permission_required('dashboard.add_sales',login_url='dashboard-index')
def salesUpdate(request,pk):
    sales = Sales.objects.get(id=pk)
    if request.method == 'POST':
        form = SalesUpdateForm(request.POST,instance=sales)
        if form.is_valid():
            sales = form.save(commit=False)
            # quantity = sales.quantity
            # price = sales.price_per
            # sales.total_price = quantity*price
            sales.save()
            return redirect('dashboard-sales')
    else:
        form = SalesUpdateForm(instance=sales)
    context = {
        'form':form,
        'sales':sales
    }
    return render(request,'dashboard/sales_update.html',context)

@permission_required('dashboard.add_purchase',login_url='dashboard-index')
def purchase(request):
    if request.method=='POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-purchase')
    else:
        form = PurchaseForm()
    context = {
        'form':form,
        'purchase_list':Purchase.objects.all().order_by('-date'),
    }
    return render(request,'dashboard/purchase.html',context)

@permission_required('dashboard.add_purchase',login_url='dashboard-index')
def purchaseUpdate(request,pk):
    purchase = Purchase.objects.get(id=pk)
    if request.method == 'POST':
        form = PurchaseUpdateForm(request.POST,instance=purchase)
        if form.is_valid():
            purchase = form.save(commit=False)
            # quantity = purchase.quantity
            # price = purchase.price_per
            # purchase.total_price = quantity*price
            purchase.save()
            return redirect('dashboard-purchase')
    else:
        form = PurchaseUpdateForm(instance=purchase)
    context = {
        'form':form,
        'purchase':purchase
    }
    return render(request,'dashboard/purchase_update.html',context)

@permission_required('dashboard.add_accounts',login_url='dashboard-index')
def accounts(request):
    total_purchased_price = 0 
    total_sold_price = 0 
    for purchase in Purchase.objects.all():
        total_purchased_price+=purchase.total_price
    for sales in Sales.objects.all():
        total_sold_price+=sales.total_price
    context = {
        'accounts_list':Accounts.objects.all(),
        'purchase_list':Purchase.objects.all().order_by('-date'),
        'sales_list':Sales.objects.all().order_by('-date'),
        'total_purchased_price':total_purchased_price,
        'total_sold_price':total_sold_price,
        'total_customers':Customer.objects.all().count(),
    }
    return render(request,'dashboard/accounts.html',context)

#Sales Data
def salesData(request):
    data = dict()
    if request.method == 'GET':
        sales_list = Sales.objects.all().order_by('-date')
        # asyncSettings.dataKey = 'table'
        data['table'] = render_to_string(
            'dashboard/_sales_table.html',
            {'sales_list': sales_list},
            request=request
        )
        return JsonResponse(data)
    
#Purchase Data
def purchaseData(request):
    data = dict()
    if request.method == 'GET':
        purchase_list = Purchase.objects.all().order_by('-date')
        # asyncSettings.dataKey = 'table'
        data['table'] = render_to_string(
            'dashboard/_purchase_table.html',
            {'purchase_list': purchase_list},
            request=request
        )
        return JsonResponse(data)

#Bootstrap Modal Form
class SalesUpdateView(BSModalUpdateView):
    model = Sales
    template_name = 'dashboard/bsmodal_sales_update.html'
    form_class = BSModalSalesUpdateForm
    success_message = 'Price was updated.'
    success_url = reverse_lazy('dashboard-sales') 

class PurchaseUpdateView(BSModalUpdateView):
    model = Purchase
    template_name = 'dashboard/bsmodal_purchase_update.html'
    form_class = BSModalPurchaseUpdateForm
    success_message = 'Price was updated.'
    success_url = reverse_lazy('dashboard-purchase')      

class CustomerReadView(BSModalReadView):
    model = Customer
    template_name = 'dashboard/read_customer.html'