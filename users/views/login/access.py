from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from users.forms.accessform import LoginForm, SignupForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirigir a la página de inicio después de iniciar sesión
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, './users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirigir a la página de inicio de sesión después de cerrar sesión

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'El nombre de usuario ya está en uso.')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    login(request, user)
                    return redirect('home')  # Redirigir a la página de inicio después de registrarse
            else:
                messages.error(request, 'Las contraseñas no coinciden.')
    else:
        form = SignupForm()
    return render(request, './users/signup.html', {'form': form})
