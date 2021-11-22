from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index,name='dashboard-index'),
    path('staff/', views.staff,name='dashboard-staff'),
    path('staff/<int:pk>/', views.staff_view,name='dashboard-staff-view'),
    path('product/', views.product,name='dashboard-product'),
    path('product/delete/<int:pk>', views.product_delete,name='dashboard-product-delete'),
    path('product/update/<int:pk>', views.product_update,name='dashboard-product-update'),
    path('order/', views.order,name='dashboard-order'),
    path('sales/', views.sales,name='dashboard-sales'),
    # path('sales/update/<int:pk>/', views.salesUpdate,name='dashboard-sales-update'),
    path('sales/update/<int:pk>/', views.SalesUpdateView.as_view(),name='dashboard-sales-update'),
    path('salesdata/',views.salesData,name='sales-data'),
    path('sales/customer_autocomplete/', views.customer_autocomplete, name='customer_autocomplete'),
    path('customer/read/<int:pk>', views.CustomerReadView.as_view(), name='read_customer'),
    path('purchase/', views.purchase,name='dashboard-purchase'),
    #path('purchase/update/<int:pk>/', views.purchaseUpdate,name='dashboard-purchase-update'),
    path('purchase/update/<int:pk>/', views.PurchaseUpdateView.as_view(),name='dashboard-purchase-update'),
    path('purchasedata/',views.purchaseData,name='purchase-data'),
    path('accounts/', views.accounts,name='dashboard-accounts'),
]
