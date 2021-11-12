from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm

from dashboard.decorators import admin_only
from .forms import CustomUserCreationForm, PermissionUpdateForm,UserUpdateForm,ProfileUpdateForm
from .decorators import unauthenticated_user
from django.contrib.auth.models import Group, User
from django.contrib.auth.models import Permission

# Create your views here.
@unauthenticated_user
def userRegister(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            permission = Permission.objects.get(name='Can add order')
            user.user_permissions.add(permission)
            username = form.cleaned_data.get('username')
            messages.success(request,f'{username} was created.')
            return redirect('user-login')
    else:
        form = CustomUserCreationForm()
    context = {
        'form':form,
    }
    return render(request,'user/register.html',context)

@login_required()
@admin_only
def adminRegister(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #user.groups.add(name='admin')
            user.is_staff = True
            user.is_superuser = True
            user.save()
            admin_group = Group.objects.get(name='admin')
            admin_group.user_set.add(user)
            username = form.cleaned_data.get('username')
            messages.success(request,f'Admin {username} was created.')
            return redirect('user-manage')
    else:
        form = CustomUserCreationForm()
    context = {
        'form':form,
    }
    return render(request,'user/admin_register.html',context)

@login_required()
@admin_only
def salesmanRegister(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #user.groups.add(name='admin')
            user.is_staff = True
            user.save()
            salesman_group = Group.objects.get(name='salesman')
            salesman_group.user_set.add(user)
            username = form.cleaned_data.get('username')
            messages.success(request,f'Sales User \'{username}\' was created.')
            return redirect('user-manage')
    else:
        form = CustomUserCreationForm()
    context = {
        'form':form,
    }
    return render(request,'user/admin_register.html',context)

@login_required()
@admin_only
def purchaseRegister(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #user.groups.add(name='admin')
            user.is_staff = True
            user.save()
            purchase_group = Group.objects.get(name='purchase')
            purchase_group.user_set.add(user)
            username = form.cleaned_data.get('username')
            messages.success(request,f'Purchase User \'{username}\' was created.')
            return redirect('user-manage')
    else:
        form = CustomUserCreationForm()
    context = {
        'form':form,
    }
    return render(request,'user/admin_register.html',context)

@login_required()
@admin_only
def accounterRegister(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #user.groups.add(name='admin')
            user.is_staff = True
            user.save()
            accounter_group = Group.objects.get(name='accounter')
            accounter_group.user_set.add(user)
            username = form.cleaned_data.get('username')
            messages.success(request,f'Accounter user \'{username}\' was created.')
            return redirect('user-manage')
    else:
        form = CustomUserCreationForm()
    context = {
        'form':form,
    }
    return render(request,'user/admin_register.html',context)

@login_required
def profile(request):
    return render(request,'user/profile.html')

@login_required
def updateProfile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form':user_form,
        'profile_form':profile_form
    }
    return render(request,'user/profile_update.html',context)

@admin_only
def manageUsers(request):
    context = {
        'staffs':User.objects.all().order_by('id')
    }
    return render(request,'user/manage_users.html',context)

@admin_only
def updatePermissions(request,id):
    staff = User.objects.get(pk=id)
    if request.method == 'POST':
        form = PermissionUpdateForm(request.POST,instance=staff)
        if form.is_valid():
            username = form.save().username
            messages.success(request,f'Permission Updated for \'{username}\' success.')
            return redirect('user-manage')
    else:
        form = PermissionUpdateForm(instance=staff)
    context = {
        'staff':staff,
        'form':form
    }
    return render(request,'user/update_permissions.html',context)