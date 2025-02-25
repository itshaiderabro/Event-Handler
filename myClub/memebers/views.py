from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm

# Create your views here.
def login_user(request):
    if request.method ==   'POST':
        username = request.POST['username']
        pasword = request.POST['password']
        user = authenticate(request, username=username, password=pasword)
        if user is not  None:
             login(request, user)
             messages.success(request, "Logged In Succesfully")
             return redirect('index')
        else:
            messages.success(request, "Your credntail doesn't match try again")
            return  redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})
    
def logout_user(request):
    logout(request)
    messages.success(request, "You have logged Out!")
    return redirect('index')

def registration_user(request):
    if request.method ==   'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            newUser = authenticate(username=user, password=password)
            login(request, newUser)
            messages.success(request, "You have registered successfully")
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'authenticate/registration.html', {'form':form})