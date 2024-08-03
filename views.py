from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from random import choice, shuffle
from aes512 import AES

crypter = AES()
key = '3421WO46rDL12e Suck134S so that the best app of the ever 135@!#$'

def index(req: WSGIRequest):
    if req.POST:
        return post_index(req)
    with open('words.txt', encoding='utf-8') as f:
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

def post_index(req):
    getted = req.POST
    print(getted)
    decrypted_right = crypter.decrypt(key, getted.get("right"))
    maybe = [getted[key] for key in getted if key.startswith('maybe')]
    if maybe:
        maybe = list(map(lambda item: crypter.decrypt(key, item), maybe))
    data = {
        'guessed': decrypted_right,
        'maybe': maybe
    }
    word = getted.get("word").lower()
    print(word, decrypted_right, maybe)
    if word == decrypted_right:
        status = 'guessed_right'
    elif word in maybe:
        status = 'guessed_maybe'
    else:
        status = 'not_guessed'
    data['status'] = status
    return render(req, 'index.html', data)
