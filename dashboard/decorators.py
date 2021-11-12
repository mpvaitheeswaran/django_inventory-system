from django.shortcuts import redirect

def admin_only(view_func):
    def wrapper_func(request,*args,**kwargs):
        group =None
        if request.user.groups.filter(name='admin').exists():
            group = request.user.groups.get(name='admin').name
        
        if group == 'admin':
            return view_func(request,*args,**kwargs)
        else:
            return redirect('dashboard-index')
    return wrapper_func

def salesman_only(view_func):
    def wrapper_func(request,*args,**kwargs):
        group = None
        if request.user.groups.filter(name='salesman').exists():
            group = request.user.groups.get(name='salesman').name
        
        if group == 'salesman':
            return view_func(request,*args,**kwargs)
        else:
            return redirect('dashboard-index')
    return wrapper_func

def purchase_only(view_func):
    def wrapper_func(request,*args,**kwargs):
        group = None
        if request.user.groups.filter(name='purchase').exists():
            group = request.user.groups.get(name='purchase').name
        
        if group == 'purchase':
            return view_func(request,*args,**kwargs)
        else:
            return redirect('dashboard-index')
    return wrapper_func

def accounter_only(view_func):
    def wrapper_func(request,*args,**kwargs):
        group = None
        if request.user.groups.filter(name='accounter').exists():
            group = request.user.groups.get(name='accounter').name
        
        if group == 'accounter':
            return view_func(request,*args,**kwargs)
        else:
            return redirect('dashboard-index')
    return wrapper_func
