from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm



def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Logged In')
            return redirect('home')
        else:
            return redirect('loginUser')
    else:
        return render(request, 'authenticate/login.html')
    
    
    
def logoutUser(request):
    logout(request)
    messages.error(request, 'Logged Out')
    return redirect('home')



def registerUser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() 
            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password1']
            username = request.POST['username']
            password = request.POST['password1']
            password1 = request.POST['password2']
            user = authenticate(username=username, password=password, password1=password1)
            login(request, user)
            messages.success(request, 'Successfully Registred')
            return redirect('home')
    else:
        form = UserCreationForm()
        
    context = {'form': form}
    return render(request, 'authenticate/register.html', context)



def resetPassword(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            email = request.POST['email']
            user = authenticate(email=email)
            login(request, user)
            messages.success(request, 'Password Sent')
            return redirect('home')
    else:
        form = UserCreationForm()
        
    context = {'form': form}
    return render(request, 'authenticate/reset_password.html', context)



def resetPasswordConfirm(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            user = authenticate(password1=password1, password2=password2)
            login(request, user)
            messages.success(request, 'Password Saved')
            return redirect('home')
    else:
        form = UserCreationForm()
        
    context = {'form': form}
    return render(request, 'authenticate/reset_password_confirm.html', context)