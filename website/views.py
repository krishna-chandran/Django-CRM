from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from .forms import SignUpForm
from .models import Record 

# Create your views here.
def home(request):
    records = Record.objects.all()
    #Check to see if logging
    if request.method == 'POST':
        user_name = request.POST['username']
        pass_word = request.POST['password']
        #Authenticate
        user = authenticate(request, username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records':records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out") 
    return render(request, 'home.html', {})

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request, user)
            messages.success(request, "You have successfully registered")
            return redirect('home')

    else:
        form = SignUpForm()
        return render(request,"register.html", {'form':form})
    return render(request,"register.html", {'form':form})

def password_reset(request):
    return render(request,"password_reset.html")

def customer_record(request,pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request,'record.html',{'customer_record':customer_record})
    else:
        messages.success(request,"You must be logged in to view the records")
        return redirect('home')
    
def add_record(request):
    return render(request,'add_record.html',{}) 