from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from users.forms.accessform import LoginForm, SignupForm
from common.models import AstradUser
import random


frases_falla = [
    "¡Parece que el nombre de usuario o la contraseña están tramando algo! ¡Vamos a poner orden por aquí!",
    "¡Oops! Parece que el nombre de usuario o la contraseña decidieron tomar un descanso. ¡Hora de hacerles regresar al trabajo!",
    "¡Algo anda raro por aquí! El nombre de usuario o la contraseña parecen estar en una especie de huelga. ¡A ver si podemos negociar con ellos!",
    "¡Vaya, vaya! El nombre de usuario o la contraseña están jugando al escondite. ¡A ver si podemos encontrarlos pronto!",
    "¡Parece que el nombre de usuario o la contraseña se fueron de parranda! ¡Vamos a traerlos de vuelta a la realidad!",
    "¡Ay caramba! Parece que el nombre de usuario o la contraseña andan de fiesta por otro lado. Vamos a ponerse serios y asegurarnos de que estén en la misma página, ¿vale?"

]


def login_view(request):
    if request.user.is_authenticated:
        return redirect('login:home')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('login:home')  # Redirigir a la página de inicio después de iniciar sesión
                else:
                    frase_aleatoria = random.choice(frases_falla)
                    messages.error(request, frase_aleatoria)
        else:
            form = LoginForm()
        return render(request, './users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login:login')  # Redirigir a la página de inicio de sesión después de cerrar sesión


frases = [
    "¡Hey, qué onda! Espero que te guste más que un gato encontrar una caja vacía.",
    "¡Hey, qué tal! Espero que disfrutes más que un niño en una tienda de golosinas.",
    "¡Hey, bienvenido! Espero que te guste tanto como a un panda le gusta el bambú.",
    "¡Ey, qué pasa! Espero que te diviertas más que un perro con dos colas.",
    "¡Hola, colega! Espero que disfrutes tanto como una abeja disfruta de una flor llena de néctar.",
    "¡Hey, bienvenido! Espero que te guste tanto como encontrar dinero en el bolsillo de un abrigo viejo.",
    "¡Hey, bienvenido! Espero que te guste tanto como un perro encuentra gustosos los zapatos nuevos para morder.",
]


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 == password2:
                if AstradUser.objects.filter(username=username).exists():
                    messages.error(request, '¡Ups! Parece que este nombre de usuario ya ha sido tomado. ¿Podrías intentar con otro?')
                else:
                    user = AstradUser.objects.create_user(username=username, email=email, password=password1)
                    login(request, user)
                    frase_aleatoria = random.choice(frases)
                    messages.success(request, frase_aleatoria)
                    return redirect('login:home')  # Redirigir a la página de inicio después de registrarse
            else:
                messages.error(request, '¡Oye, las contraseñas no se están poniendo de acuerdo aquí! Vamos, ustedes dos, ¡pongan de su parte y coincidan de una vez!')
    else:
        form = SignupForm()
    return render(request, './users/signup.html', {'form': form})



