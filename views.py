from django.contrib.auth import authenticate as auth, login, logout, get_user
from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from users.models import Profile
from scrumble_site.forms import RegisterForm, LoginForm

def logout_required(func):
    def wrapper(req, *args, **kwargs):
        if get_user(req).is_authenticated and req.method == "GET":
            return redirect('index', permanent=True)
        return func(req, *args, **kwargs)
    return wrapper

@logout_required
def register_root(req: WSGIRequest):
    if req.method == 'GET':
        form = RegisterForm()
        return render(req, 'register.html', {'form': form})
    elif req.method == 'POST':
        form = RegisterForm(req.POST) 
        if not form.is_valid():
            return render(req, 'register.html', {'form': form})
        user = form.save(commit=False)
        user.username = user.username.lower()
        user.save()
        profile = Profile()
        profile.user = user
        profile.lose, profile.win = 0, 0
        profile.save()
        login(req, user)
        return redirect('index', permanent=True)

def check_logout(req: WSGIRequest):
    if "logout" in req.POST.keys():
        logout(req)
        return True

def validate_form(req: WSGIRequest):
    form = LoginForm(req.POST)
    if not form.is_valid():
        print(form.errors)
        return False, form
    username, password = list(form.data.values())[1:]
    user = auth(username=username, password=password)
    if user is None or not user.check_password(password):
        form.add_error("password", "Неверный пароль или логин")
        form.add_error("username", "Неверный пароль или логин")
        return False, form
    return True, user

@logout_required
def login_root(req: WSGIRequest):
    if req.method == 'GET':
        return render(req, 'login.html', {'form': LoginForm()})
    elif req.method == 'POST':
        if check_logout(req):
            return redirect('login', permanent=True)
        status, item = validate_form(req)
        if not status:
            return render(req, 'login.html', {'form': item})
        login(req, item)
        return redirect('index', permanent=True)
