from django.shortcuts import render, redirect
from .decorators import unauthenticated_user
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


@unauthenticated_user
def registorPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            messages.success(request, 'Аккаунт успешно создан ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'main/register.html', context)


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Имя пользователя или пароль некорректны')


    context = {}
    return render(request, 'main/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):
    data = {
        'title': 'Главная страница'
    }
    return render(request, 'main/index.html', data)


@login_required(login_url='login')
def about(request):
    return render(request, 'main/about.html')


@login_required(login_url='login')
def contacts(request):
    return render(request, 'main/contacts.html')
