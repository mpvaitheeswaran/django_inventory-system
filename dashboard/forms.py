from django.forms import fields
from .models import Accounts, Order, Product, Purchase, Sales
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column,HTML

class DateInput(forms.DateInput):
    input_type = 'date'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','category','quantity']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product','order_quantity']

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'
        widgets = {
            'date': DateInput()
        }
    
    def __init__(self, *args, **kwargs):
        super(PurchaseForm, self).__init__(*args, **kwargs)
        self.fields['price_per'].label = "Price per Quantity"

        self.helper = FormHelper()
        self.helper.layout = Layout(
                'date',
                'product',
                'supplier_name',
                Row(
                    Column('quantity', css_class='col mb-0'),
                    Column(HTML('<p>X</p>'), css_class='col-sm-1 mb-0'),
                    Column('price_per', css_class=' col mb-0 '),
                    css_class='row justify-content-between align-items-end'
                ),
                'total_price',
                Submit('submit', 'Add',css_class='btn btn-success w-100 mt-2'),
               
        )

class SalesForm(forms.ModelForm):
    
    class Meta:
        model = Sales
        fields = ['date','purchase','customer_name','quantity','price_per','total_price']
        widgets = {
            'date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(SalesForm, self).__init__(*args, **kwargs)
        self.fields['purchase'].label = "Product"
        self.fields['price_per'].label = "Price per Quantity"

        self.helper = FormHelper()
        self.helper.layout = Layout(
                'date',
                'purchase',
                'customer_name',
                Row(
                    Column('quantity', css_class='col mb-0'),
                    Column(HTML('<p>X</p>'), css_class='col-sm-1 mb-0'),
                    Column('price_per', css_class=' col mb-0 '),
                    css_class='row justify-content-between align-items-end'
                ),
                'total_price',
                Submit('submit', 'Add',css_class='btn btn-success w-100 mt-2'),
               
        )
class SalesUpdateForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['quantity','price_per','total_price']
    
    def __init__(self, *args, **kwargs):
        super(SalesUpdateForm, self).__init__(*args, **kwargs)
        self.fields['price_per'].label = "Price per Quantity"

        self.helper = FormHelper()
        self.helper.layout = Layout(
                Row(
                    Column('quantity', css_class='col mb-0'),
                    Column(HTML('<p>X</p>'), css_class='col-sm-1 mb-0'),
                    Column('price_per', css_class=' col mb-0 '),
                    css_class='row justify-content-between align-items-end'
                ),
                'total_price',
                Submit('submit', 'Update',css_class='btn btn-success w-100 mt-2'),    
        )

class PurchaseUpdateForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['quantity','price_per','total_price']
    
    def __init__(self, *args, **kwargs):
        super(PurchaseUpdateForm, self).__init__(*args, **kwargs)
        self.fields['price_per'].label = "Price per Quantity"

        self.helper = FormHelper()
        self.helper.layout = Layout(
                Row(
                    Column('quantity', css_class='col mb-0'),
                    Column(HTML('<p>X</p>'), css_class='col-sm-1 mb-0'),
                    Column('price_per', css_class=' col mb-0 '),
                    css_class='row justify-content-between align-items-end'
                ),
                'total_price',
                Submit('submit', 'Update',css_class='btn btn-success w-100 mt-2'),    
        )

class AccountsForm(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = ['sales','purchase_price']