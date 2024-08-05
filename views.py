from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.decorators import login_required
from scrumble_site.forms import RegisterForm, LoginForm
from random import choice, shuffle
from utils.aes512 import AES
from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

crypter = AES()
key = getenv("KEY")

@login_required(login_url='/login')
def index(req: WSGIRequest):
    if req.POST:
        return post_index(req)
    with open('data/words.txt', encoding='utf-8') as f:
        WORDS = f.read().splitlines()
    right = choice(WORDS)
    WORDS.remove(right)
    shuffled = sorted(right)
    maybe = [word for word in WORDS if shuffled == sorted(word)]
    while shuffled == sorted(right):
        shuffle(shuffled)
    encrypted_right, encrypted_maybe = crypter.encrypt(key, right), list(map(lambda d: crypter.encrypt(key, d), maybe))
    data = {
        'status': 'guessing',
        'word': ''.join(shuffled),
        'encrypted_right': encrypted_right,
        'encrypted_maybe': encrypted_maybe,
        'len': len(shuffled)
    }
    return render(req, 'index.html', data)

def post_index(req: WSGIRequest):
    getted = req.POST
    decrypted_right = crypter.decrypt(key, getted.get("right"))
    maybe = [getted[key] for key in getted if key.startswith('maybe')]
    if maybe:
        maybe = list(map(lambda item: crypter.decrypt(key, item), maybe))
    data = {
        'guessed': decrypted_right,
        'maybe': maybe
    }
    word = getted.get("word").lower()
    if word == decrypted_right:
        status = 'guessed_right'
    elif word in maybe:
        status = 'guessed_maybe'
    else:
        status = 'not_guessed'
    data['status'] = status
    return render(req, 'index.html', data)

def register(req: WSGIRequest):
    if req.method == 'GET':
        form = RegisterForm()
        return render(req, 'register.html', {'form': form})
    elif req.method == 'POST':
        form = RegisterForm(req.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('index')
        else:
            return render(req, 'register.html', {'form': form})


def login(req: WSGIRequest):
    if req.method == 'GET':
        return render(req, 'login.html', {'form': LoginForm()})
    elif req.method == 'POST':
        form = RegisterForm(req.POST) 
        if not form.is_valid():
            return render(req, 'login.html', {'form': form})
        user = form.save(commit=False)
        user.username = user.username.lower()
        user.save()
        return redirect('index')
            