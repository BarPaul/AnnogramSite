from django.shortcuts import render
from django.contrib.auth import get_user, decorators
from django.core.handlers.wsgi import WSGIRequest
from users.models import Profile
from random import choice, shuffle
from utils.aes512 import AES
from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

crypter = AES()
key = getenv("KEY")

@decorators.login_required(login_url='/login')
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
    user = get_user(req)
    data = {
        'status': 'guessing',
        'word': ''.join(shuffled),
        'encrypted_right': encrypted_right,
        'encrypted_maybe': encrypted_maybe,
        'len': len(shuffled),
        'user': user
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
    profile = Profile.objects.get(user=get_user(req))
    profile.win += 1
    if word == decrypted_right:
        status = 'guessed_right'
    elif word in maybe:
        status = 'guessed_maybe'
    else:
        status = 'not_guessed'
        profile.win, profile.lose = profile.win - 1, profile.lose + 1
    data['status'] = status
    profile.save()
    return render(req, 'index.html', data)
