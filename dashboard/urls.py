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
    path('sales/update/<int:pk>/', views.salesUpdate,name='dashboard-sales-update'),
    path('purchase/', views.purchase,name='dashboard-purchase'),
    path('accounts/', views.accounts,name='dashboard-accounts'),
]
